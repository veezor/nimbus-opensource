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

from django.conf import settings

from nimbus.schedules.models import Schedule
from nimbus.filesets.models import FileSet
from nimbus.computers.models import Computer
from nimbus.procedures.models import Procedure


class Trashmen(object):
    """Dont you know about a bird? Everybody that bird is a word!"""

    def orphan_objects(self):
        """Pega todos os objetos orfaos"""
        orphans = []
        # Schedules que não são modelos e não tem procedure
        schedules = Schedule.objects.filter(is_model=False,procedures__isnull=True)
        orphans += schedules
        
        # Filesets que não são modelos e não tem procedure
        filesets = FileSet.objects.filter(is_model=False,procedures__isnull=True)
        orphans += filesets

        return orphans
        
    def remove_orphan_objects(self):
        """Remove todos os objetos orfaos"""
        orphans = self.orphan_objects()
        for orphan in orphans:
            orphan.delete()

    def orphan_files(self):
        orphans = []
        orphans += self.orphan_computer_files()
        orphans += self.orphan_fileset_files()
        orphans += self.orphan_schedule_files()
        orphans += self.orphan_procedure_files()
        orphans += self.orphan_pool_files()
        return orphans

    def remove_orphan_files(self):
        orphans = self.orphan_files()
        for orphan in orphans:
            os.remove(orphan)
        
    def orphan_computer_files(self):
        orphans = []
        dir_path = settings.NIMBUS_COMPUTERS_DIR
        files = os.listdir(dir_path)
        computers = Computer.objects.all()
        computer_names = [computer.bacula_name for computer in computers]
        for f in files:
            if f not in computer_names:
                orphans.append("%s/%s" % (dir_path, f))
        return orphans
        
    def orphan_fileset_files(self):
        orphans = []
        dir_path = settings.NIMBUS_FILESETS_DIR
        files = os.listdir(dir_path)
        filesets = FileSet.objects.all()
        fileset_names = [fileset.bacula_name for fileset in filesets]
        for f in files:
            if f not in fileset_names:
                orphans.append("%s/%s" % (dir_path, f))
        return orphans

    def orphan_schedule_files(self):
        orphans = []
        dir_path = settings.NIMBUS_SCHEDULES_DIR
        files = os.listdir(dir_path)
        schedules = Schedule.objects.all()
        schedule_names = [schedule.bacula_name for schedule in schedules]
        for f in files:
            if f not in schedule_names:
                orphans.append("%s/%s" % (dir_path, f))
        return orphans

    def orphan_procedure_files(self):
        orphans = []
        dir_path = settings.NIMBUS_JOBS_DIR
        files = os.listdir(dir_path)
        procedures = Procedure.objects.all()
        procedure_names = [procedure.bacula_name for procedure in procedures]
        for f in files:
            if f not in procedure_names:
                orphans.append("%s/%s" % (dir_path, f))
        return orphans

    def orphan_pool_files(self):
        orphans = []
        dir_path = settings.NIMBUS_POOLS_DIR
        files = os.listdir(dir_path)
        procedures = Procedure.objects.all()
        pool_names = [procedure.pool_bacula_name() for procedure in procedures]
        for f in files:
            if f not in pool_names:
                orphans.append("%s/%s" % (dir_path, f))
        return orphans
