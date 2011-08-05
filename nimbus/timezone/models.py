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



import re
import logging
import time
from operator import itemgetter
from xmlrpclib import ServerProxy


from pytz import country_names

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.core.exceptions import ValidationError


from nimbus.shared import signals
from nimbus.libs import systemprocesses
from nimbus.base.models import UUIDSingletonModel as BaseModel


DOMAIN_RE = re.compile(r"^(\w+\.)?\w+\.\w+$")

EMPTY_CHOICES = [('', '----------')]

COUNTRY_CHOICES = [ item \
                    for item in \
                    sorted(country_names.items(), key=itemgetter(1)) ]


def check_domain(value):
    if not DOMAIN_RE.match(value):
        raise ValidationError("ntp_server must be a domain")



class Timezone(BaseModel):
    ntp_server = models.CharField('Servidor ntp', max_length=255, blank=False,
                                   null=False, default="a.ntp.br",
                                   validators=[check_domain])
    country = models.CharField('País', max_length=255, blank=False, 
                                choices=COUNTRY_CHOICES)
    area = models.CharField('Região', max_length=255, blank=False, 
                             null=False)


    class Meta:
        verbose_name = u"Fuso horário"


    
class InvalidTimezone(Exception):
    pass


def update_system_timezone(timezone):

    def callable(timezone):
        try:
            server = ServerProxy(settings.NIMBUS_MANAGER_URL)
            server.change_timezone(timezone.area)
            time.tzset()
        except Exception, error:
            logger = logging.getLogger(__name__)
            logger.exception("Conexao com nimbus-manager falhou")


    systemprocesses.norm_priority_job( "Set system timezone", 
                                        callable, timezone)


def update_ntp_cron_file(timezone):

    def callable(timezone):
        try:
            server = ServerProxy(settings.NIMBUS_MANAGER_URL)
            server.generate_ntpdate_file_on_cron(timezone.ntp_server)
        except Exception, error:
            logger = logging.getLogger(__name__)
            logger.exception("Conexao com nimbus-manager falhou")


    systemprocesses.norm_priority_job( "Generate ntpdate cron file", 
                                        callable, timezone)




signals.connect_on( update_system_timezone, Timezone, post_save )
signals.connect_on( update_ntp_cron_file, Timezone, post_save )
