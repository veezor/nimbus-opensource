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



from os import path
import logging
import xmlrpclib

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.conf import settings


from pybacula import configcheck

from nimbus.base.models import BaseModel
from nimbus.shared import utils, signals, fields
from nimbus.libs.template import render_to_file
from nimbus.config.models import Config
from nimbus.network.models import get_nimbus_address
from nimbus.computers.models import Computer






class Storage(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False,
                            validators=[fields.check_model_name])
    address = models.IPAddressField(default=get_nimbus_address, editable=False,
                                    null=False, blank=False)
    password = models.CharField( max_length=255, null=False, 
                                 blank=False, editable=False,
                                 default=utils.random_password)

    description = models.TextField(max_length=500, blank=True)
    active = models.BooleanField(editable=False)



    class Meta:
        verbose_name = u"Dispositivo de armazenamento"

    @property
    def is_local(self):
        if self.address == get_nimbus_address():
            return True
        return False
        

    def __unicode__(self):
        return u"(%s:%s)" % (
            self.name,
            self.address)
    
    @property
    def get_computers(self):
        """Computadores que fazem backup neste storage."""
        computers = Computer.objects.filter(procedure__storage=self).\
            order_by('name').distinct()
        
        # computers = []
        # for profile in self.profile_set.all():
        #     for procedure in profile.procedure_set.all():
        #         computers.append(procedure.computer)
        # 
        # sorted(computers, key=lambda computer: computer.name)
        return computers


class Device(BaseModel):
    name = models.CharField(max_length=255, null=False,
                            validators=[fields.check_model_name])
    archive = fields.ModelPathField(max_length=2048, null=False)
    storage = models.ForeignKey(Storage, null=False, related_name="devices")

    @property
    def is_local(self):
        return self.storage.is_local


    def __unicode__(self):
        return "%s in %s" % (self.name, self.archive)



def update_storage_file(storage):
    """Update storage File"""

    filename = settings.BACULASD_CONF 

    if storage.is_local and storage.active:
        try:
            logger = logging.getLogger(__name__)

            config = Config.objects.get(id=1)

            render_to_file( filename,
                            "bacula-sd",
                            name=storage.bacula_name,
                            port=9103,
                            max_cur_jobs=100,
                            director_name=config.director_name,
                            director_password=storage.password,
                            devices_dir=settings.NIMBUS_DEVICES_DIR)

            logger.info("Arquivo de configuracao do storage gerado com sucesso")
        except Config.DoesNotExist, error:
            logger.info("Config does not exist")




def create_default_device(storage):

    if storage.devices.count() == 0:
        device = Device.objects.create(name="device default",
                                       archive="/bacula/",
                                       storage=storage)
        storage.devices.add(device)


def update_device_file(device):

    try:
        if device.storage.active:

            name = device.bacula_name
            storagename = device.storage.bacula_name

            filename = path.join( settings.NIMBUS_DEVICES_DIR, 
                                  name)
            
            storagefile = path.join( settings.NIMBUS_STORAGES_DIR, 
                                  storagename)

            render_to_file( filename,
                            "device",
                            name=name,
                            archive_device=device.archive)

            render_to_file( storagefile,
                            "storages",
                            devices=Device.objects.all())
    except Storage.DoesNotExist:
        pass #loaddata



def update_storage_devices(storage):
    for device in storage.devices.all():
        update_device_file(device)



def remove_device_file(device):

    if device.storage.active:
        name = device.bacula_name

        filename = path.join( settings.NIMBUS_DEVICES_DIR, 
                              name)
        storagefile = path.join( settings.NIMBUS_STORAGES_DIR, 
                              name)

        utils.remove_or_leave(filename)
        utils.remove_or_leave(storagefile)



def restart_bacula_storage(model):
    try:
        logger = logging.getLogger(__name__)
        configcheck.check_baculasd(settings.BACULASD_CONF)
        manager = xmlrpclib.ServerProxy(settings.NIMBUS_MANAGER_URL)
        stdout = manager.storage_restart()
        logger.info(stdout)
    except configcheck.ConfigFileError, error:
        logger.error('Bacula-sd error, not reloading')
    except Exception, error:
        logger.error("Reload bacula-sd error")



signals.connect_on( update_storage_file, Storage, post_save)
signals.connect_on( update_storage_devices, Storage, post_save)
signals.connect_on( restart_bacula_storage, Storage, post_save)
signals.connect_on( create_default_device, Storage, post_save)
signals.connect_on( update_device_file, Device, post_save)
signals.connect_on( restart_bacula_storage, Device, post_save)
signals.connect_on( remove_device_file, Device, post_delete)
