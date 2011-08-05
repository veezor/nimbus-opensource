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




from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic



class AdministrativeModel(models.Model):
    content_type = models.ForeignKey(ContentType, null=False, blank=False)
    object_id = models.PositiveIntegerField(null=False, blank=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')



def register_object(model):
    adm_model = AdministrativeModel.objects.create(content_object=model)


def register_object_from_id(content_type, object_id):
    model_object = content_type.get_object_for_this_type(id=object_id)
    return register_object(model_object)


def register_object_from_model_name(app_label, model_name, object_id):
    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
    return register_object_from_id( content_type, object_id)


def register_objects_from_tuple(*args):
    for app_label, model_name, object_id in args:
        register_object_from_model_name(app_label, model_name, object_id)


def register_administrative_nimbus_models():
    register_objects_from_tuple(
            ("computers", "computer", 1),
            ("computers", "cryptoinfo", 1),
            ("filesets", "fileset", 1),
            ("filesets", "filepath", 1),
            ("filesets", "filepath", 2),
            ("filesets", "filepath", 3),
            ("filesets", "filepath", 4),
            ("schedules", "schedule", 1),
            ("schedules", "run", 1),
            ("schedules", "run", 2),
            ("schedules", "backupkind", 1),
            ("schedules", "backupkind", 2),
            ("schedules", "backupkind", 3),
            ("schedules", "backupkind", 4),
            ("schedules", "backuplevel", 1),
            ("schedules", "backuplevel", 2),
            ("procedures", "procedure", 1),
            ("storages", "storage", 1),
            ("storages", "device", 1),
    )


