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

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete, m2m_changed

from nimbus.base.models import BaseModel
from nimbus.shared import utils, signals, fields
from nimbus.computers import models as computer_models
from nimbus.libs.template import render_to_file

class FileSet(BaseModel):
    name = models.CharField(max_length=255, null=False)
    is_model = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = u"Conjunto de arquivos"

class FilePath(models.Model):
#    computer = models.ForeignKey(computer_models.Computer)
    path = fields.ModelPathField(max_length=2048, null=False)
    fileset = models.ForeignKey(FileSet, related_name="files", null=False,
                                 blank=False)

    def __unicode__(self):
        return u"%s - %s" % (self.fileset.name, self.path)


    class Meta:
        verbose_name = u"Arquivo"


def update_fileset_file(fileset):
    """FileSet update filesets to a procedure instance"""
    name = fileset.bacula_name
    filename = path.join(settings.NIMBUS_FILESETS_DIR, name)
    files = [f.path for f in fileset.files.all()]
    render_to_file(filename, "fileset", name=name, files=files)


def remove_fileset_file(fileset):
    """remove FileSet file"""
    name = fileset.bacula_name
    filename = path.join(settings.NIMBUS_FILESETS_DIR, name)
    utils.remove_or_leave(filename)    


def update_filepath(filepath):
    update_fileset_file(filepath.fileset)


signals.connect_on(update_fileset_file, FileSet, post_save)
signals.connect_on(update_filepath, FilePath, post_save)
signals.connect_on(remove_fileset_file, FileSet, post_delete)
signals.connect_on(update_filepath, FilePath, post_delete)
