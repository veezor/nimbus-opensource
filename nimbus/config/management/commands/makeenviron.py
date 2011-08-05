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



import os
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):                                                                                                                                
    args = "prefix"
    help = "Generate and test nimbus directories."
    requires_model_validation = False

    def handle(self, *args, **options):
        prefix = ""
        if len(args) == 0:
            pass
        elif len(args) == 1:
            prefix = args[0]
        else:
            raise CommandError("makeenviron requires just one argument")

        members = dir(settings)
        directories = [member for member in members if member.endswith("_DIR")]
        directories = [getattr(settings, dr) for dr in directories]
        directories.remove(settings.FILE_UPLOAD_TEMP_DIR) 
        for d in directories:
            try:
                if prefix:
                    d = prefix + "/" + d
                print d
                os.makedirs(d)
            except OSError, error:
                if (error.strerror == "FileExists" and \
                        not os.access(d, os.W_OK)) or\
                        error.strerror == "Permission denied":
                    raise CommandError("%s is not writable" % d)

        if prefix:
            etc_dir = prefix +  '/' + settings.NIMBUS_ETC_DIR
        else:
            etc_dir = settings.NIMBUS_ETC_DIR
 
        shutil.copy(settings.NIMBUS_UNDEPLOYED_LOG_CONF, 
                    etc_dir)
