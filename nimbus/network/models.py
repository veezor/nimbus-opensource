#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Copyright © 2010, 2011 Veezor Network Intelligence (Linconet Soluções em Informática Ltda.), <www.veezor.com>
#
# This file is part of Nimbus Opensource Backup.
#
#    Nimbus Opensource Backup is free software: you can redistribute it and/or 
#    modify it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License.
#
#    Nimbus Opensource Backup is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Nimbus Opensource Backup.  If not, see <http://www.gnu.org/licenses/>.
#
#In this file, along with the Nimbus Opensource Backup code, it may contain 
#third part code and software. Please check the third part software list released 
#with every Nimbus Opensource Backup copy.
#
#You can find the correct copyright notices and license informations at 
#their own website. If your software is being used and it's not listed 
#here, or even if you have any doubt about licensing, please send 
#us an e-mail to law@veezor.com, claiming to include your software.
#



import logging
from xmlrpclib import ServerProxy
from IPy import IP
import time
import networkutils

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError

from nimbus.shared import signals
from nimbus.libs import systemprocesses, bacula
from nimbus.base.models import UUIDSingletonModel as BaseModel
# TODO:
# Config importado em update_director_address() e get_nimbus_address()
# Por problemas com imports cruzados. Descobrir o jeito certo de fazer isso
# from nimbus.config.models import Config
# from nimbus.storages.models import Storage
# from nimbus.computers.models import Computer


class NetworkInterface(BaseModel):
    address = models.IPAddressField('Endereço IP', null=False)
    netmask = models.IPAddressField('Máscara de rede', null=False)
    gateway = models.IPAddressField('Gateway', null=False)
    dns1 = models.IPAddressField('Servidor DNS1', null=False)
    dns2 = models.IPAddressField('Servidor DNS2', blank=True,null=True)


    class Meta:
        verbose_name = u"Interface de rede"

    def __init__(self, *args, **kwargs):
        super(NetworkInterface, self).__init__(*args, **kwargs)
        if not self.id:
            raw_iface = networkutils.get_interfaces()[0]
            self.address = raw_iface.addr
            self.netmask = raw_iface.netmask
            self.gateway = self.default_gateway
            self.dns1 = self.default_gateway

    def clean(self):
        raw_iface = networkutils.get_interfaces()[0]
        if self.address == raw_iface.addr:
            return
        returncode, stdout = networkutils.ping(self.address, packets=1)
        if not returncode:
            raise ValidationError(u'Erro, existe outra máquina com o mesmo IP na rede.')

    def __unicode__(self):
        return u"%s/%s" % (self.address, self.netmask)

    def _get_net_object(self):
        net = IP(self.address).make_net(self.netmask)
        return net

    @property
    def broadcast(self):
        net = self._get_net_object()
        return str(net.broadcast())

    @property
    def network(self):
        net = self._get_net_object()
        return str(net.net())

    @property
    def default_gateway(self):
        net = self._get_net_object()
        return str(net[1])


def update_networks_file(interface):
    def callable(interface):
        try:
            time.sleep(10) # for redirect page
            server = ServerProxy(settings.NIMBUS_MANAGER_URL)
            server.generate_interfaces("eth0", 
                                       interface.address, 
                                       interface.netmask, 
                                       "static",
                                       interface.broadcast, 
                                       interface.network, 
                                       interface.gateway)
            server.generate_dns(interface.dns1, 
                                 interface.dns2)
            server.network_restart()
        except Exception, error:
            logger = logging.getLogger(__name__)
            logger.exception("Conexao com nimbus-manager falhou")

    if interface.address != get_raw_network_interface_address():
        systemprocesses.norm_priority_job("Generate network conf files and restart networking", 
                                         callable, interface)


def update_director_address(interface):
    from nimbus.config.models import Config # Ver nota nos imports iniciais
    
    config = Config.get_instance()
    config.director_address = interface.address
    config.save(system_permission=True)
    logger = logging.getLogger(__name__)
    logger.info("Atualizando ip do director")

def update_storage_address(interface):
    from nimbus.storages.models import Storage # Ver nota nos imports iniciais
    
    storage = Storage.objects.get(id=1) # storage default
    storage.address = interface.address
    storage.save(system_permission=True)
    logger = logging.getLogger(__name__)
    logger.info("Atualizando ip do storage")

def update_nimbus_client_address(interface):
    from nimbus.computers.models import Computer # Ver nota nos imports iniciais
    
    computer = Computer.objects.get(id=1) # storage default
    computer.address = interface.address
    computer.save(system_permission=True)
    logger = logging.getLogger(__name__)
    logger.info("Atualizando ip do client nimbus")

def get_nimbus_address():
    from nimbus.config.models import Config # Ver nota nos imports iniciais
    
    config = Config.get_instance()
    if not config.director_address:
        return get_raw_network_interface_address()
    return config.director_address

def get_raw_network_interface_address():
    raw_iface = networkutils.get_interfaces()[0]
    return raw_iface.addr

signals.connect_on(update_networks_file, NetworkInterface, post_save)
signals.connect_on(update_director_address, NetworkInterface, post_save)
signals.connect_on(update_storage_address, NetworkInterface, post_save)
signals.connect_on(update_nimbus_client_address, NetworkInterface, post_save)
