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
from datetime import datetime
import uuid
from django.db import models
from django.conf import settings
from nimbus.security.lib import check_permission
from nimbus.base.exceptions import UUIDViolation

UUID_NONE="none"
logger = logging.getLogger(__name__)


class SingletonBaseModel(models.Model):

    @classmethod
    def get_instance(cls):
        try:
            instance = cls.objects.get(pk=1)
        except cls.DoesNotExist:
            if settings.LOG_DEBUG:
                logger.info("get_instance called. Instance of %s not exist." % cls.__name__)
            instance = cls()
        return instance

    @classmethod
    def exists(cls):
        return cls.objects.all().count() > 0

    def save(self, *args, **kwargs):
        self.id = 1
        return super(SingletonBaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class UUID(models.Model):
    uuid_hex = models.CharField(editable=False,
                                max_length=255,
                                unique=True,
                                default=UUID_NONE)
    created_on = models.DateTimeField(editable=False, default=datetime.now)

    def __unicode__(self):
        return u"%s %s" % (self.uuid_hex, self.created_on)

    def save(self, *args, **kwargs):
        if self.uuid_hex == UUID_NONE:
            self.uuid_hex = uuid.uuid4().hex
            return super(UUID, self).save(*args, **kwargs)
        else:
            if settings.LOG_DEBUG:
                logger.error("UUIDViolation on %s" % self.__class__.__name__)
            raise UUIDViolation() 


class UUIDBaseModel(models.Model):
    uuid = models.ForeignKey(UUID, editable=False)

    def _generate_uuid(self):
        uuid = UUID()
        uuid.save()
        self.uuid = uuid

    def save(self, *args, **kwargs):
        try:
            self.uuid
        except UUID.DoesNotExist:
            self._generate_uuid()
        system_permission = kwargs.pop("system_permission", False)
        if not system_permission:
            check_permission(self)
        return super(UUIDBaseModel, self).save(*args, **kwargs)
 
    @property
    def bacula_name(self):
        return "%s_%s" % (self.uuid.uuid_hex, 
                          self.__class__.__name__.lower())
 
    class Meta:
        abstract = True


class UUIDSingletonModel(UUIDBaseModel, SingletonBaseModel):

   class Meta:
        abstract = True

   def save(self, *args, **kwargs):
       super(UUIDSingletonModel, self).save(*args, **kwargs)


BaseModel = UUIDBaseModel