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
import os
from os import path
from os.path import join, exists

from django.utils.translation import ugettext as _
from django.db import models, connections
from django.conf import settings
from django.db.models.signals import post_save, post_delete, pre_save 

from pybacula import BConsoleInitError

from nimbus.base.models import BaseModel
from nimbus.computers.models import Computer
from nimbus.storages.models import Storage
from nimbus.filesets.models import FileSet
from nimbus.schedules.models import Schedule
from nimbus.bacula.models import Media, Job, File
# from nimbus.pools.models import Pool
from nimbus.libs.template import render_to_file
from nimbus.libs.bacula import Bacula, ReloadManager
from nimbus.shared import utils, enums, signals, fields


class Procedure(BaseModel):
    pool_name = models.CharField(max_length=255)
    pool_size = models.FloatField(blank=False, null=False, default=5242880,
                                  editable=False)
    pool_retention_time = models.IntegerField(verbose_name=_("Retention Time (days)"),
                                              blank=False, null=False,
                                              default=30)
    computer = models.ForeignKey(Computer, verbose_name=_("Computador"),
                                 blank=False, null=False)
    active = models.BooleanField(default=True, blank=True, null=False)
    schedule = models.ForeignKey(Schedule, verbose_name=_("Schedule"),
                                 related_name='procedures')
    fileset = models.ForeignKey(FileSet, verbose_name=_("Fileset"),
                                related_name='procedures')
    storage = models.ForeignKey(Storage, verbose_name=_("Dispositivo de Armazenamento"), null=False,
                                blank=False)
    name = models.CharField(verbose_name=_("Name"), max_length=255, blank=False,
                            null=False)


    class Meta:
        verbose_name = u"Procedimento"


    def fileset_bacula_name(self):
        return self.fileset.bacula_name
        # return self.profile.fileset.bacula_name
    
    def restore_bacula_name(self):
        return "%s_restorejob" % self.uuid.uuid_hex
        
    def schedule_bacula_name(self):
        return self.schedule.bacula_name
        # return self.profile.schedule.bacula_name

    def storage_bacula_name(self):
        return self.storage.bacula_name
        # return self.profile.storage.bacula_name

    def pool_bacula_name(self):
        return '%s_pool' % self.bacula_name

    def last_success_date(self):
        return Job.objects.filter(name=self.bacula_name,jobstatus='T')\
                .order_by('-endtime')[0]

    @property
    def jobs_id_to_cancel(self):
        status = ('R','p','j','c','d','s','M','m','s','F','B', 'C') #TODO: refactor
        return Job.objects.filter(name=self.bacula_name,
                                  jobstatus__in=status).values_list('jobid', flat=True)

    @property
    def all_my_jobs(self):
        jobs = Job.objects.filter(name=self.bacula_name)
        return jobs

    @property
    def all_my_good_jobs(self):
        jobs = Job.objects.filter(name=self.bacula_name, jobstatus="T").order_by('-starttime')
        return jobs
        
    @classmethod
    def all_jobs(cls):
        job_names = [ p.bacula_name for p in cls.objects.all() ]
        jobs = Job.objects.select_related().filter(name__in=job_names).order_by('-starttime')
        return jobs

    @classmethod
    def all_non_self_jobs(cls):
        job_names = [ p.bacula_name for p in cls.objects.exclude(id=1) ]
        jobs = Job.objects.select_related().filter(name__in=job_names).order_by('-starttime')
        return jobs

    def restore_jobs(self):
        return Job.objects.filter(client__name=self.computer.bacula_name,
                                  fileset__fileset=self.fileset_bacula_name,
                                  jobstatus='T').order_by('-endtime').distinct()[:15]

    def get_backup_jobs_between(self, start, end):
        jobs = Job.objects.filter(realendtime__range=(start,end), 
                                  jobfiles__gt=0, 
                                  jobstatus='T',
                                  type='B',
                                  name=self.bacula_name)\
                                                .order_by('-endtime').distinct()
        return jobs

    def __unicode__(self):
        return self.name 

    def run(self):
        bacula = Bacula()
        bacula.run_backup(self.bacula_name, 
                          client_name=self.computer.bacula_name)
   
    @staticmethod
    def list_files(jobid, computer, path="/"):
        if path == "":
            path = "/"
        bacula = Bacula()

        if computer.operation_system == "windows" and path == '/':
            files = File.objects.filter(job=jobid,
                                       path__path__isnull=False)\
                    .extra(select={'driver': 'substr( "path"."path", 0, 4)'})\
                    .values_list('driver', flat=True).distinct()
            return list(files)

        return bacula.list_files(jobid, path)



    @staticmethod
    def search_files(jobid, pattern):
        files = File.objects.filter(
                models.Q(filename__name__icontains=pattern) | models.Q(
                path__path__icontains=pattern), job__jobid=jobid).distinct()
        files = [f.fullname for f in files]
        files.sort()
        return files


def update_procedure_file(procedure):
    """Procedure update file"""
    name = procedure.bacula_name
    filename = join(settings.NIMBUS_JOBS_DIR, name)
    render_to_file(filename,
                   "job",
                   name=name,
                   schedule=procedure.schedule_bacula_name(),
                   storage=procedure.storage_bacula_name(),
                   fileset=procedure.fileset_bacula_name(),
                   priority="10",
                   active=procedure.active,
                   client=procedure.computer.bacula_name,
                   pool=procedure.pool_bacula_name() )


    update_pool_file(procedure)

    if not exists(settings.NIMBUS_RESTORE_FILE):
        render_to_file(settings.NIMBUS_RESTORE_FILE,
                       "restore",
                       name=name + "restore",
                       storage=procedure.storage_bacula_name(),
                       fileset=procedure.fileset_bacula_name(),
                       client=procedure.computer.bacula_name,
                       pool=procedure.pool_bacula_name())

    reload_manager = ReloadManager()
    reload_manager.force_reload()

def remove_procedure_file(procedure):
    """remove procedure file"""
    base_dir,filepath = utils.mount_path(procedure.bacula_name,
                                         settings.NIMBUS_JOBS_DIR)
    utils.remove_or_leave(filepath)
    remove_pool_file(procedure)


def remove_procedure_volumes(procedure):
    pool_name = procedure.pool_bacula_name()
    medias = Media.objects.filter(pool__name=pool_name).distinct()
    volumes = [m.volumename for m in medias]
    try:
        bacula = Bacula()
        bacula.cancel_procedure(procedure)
        bacula.purge_volumes(volumes, pool_name)
        bacula.truncate_volumes(pool_name)
        bacula.delete_pool(pool_name)
        for volume in volumes:
            volume_abs_path = join(settings.NIMBUS_DEFAULT_ARCHIVE, volume)
            if exists(volume_abs_path):
                os.remove(volume_abs_path)

        reload_manager = ReloadManager()
        reload_manager.force_reload()

    except BConsoleInitError, error:
        logger = logging.getLogger(__name__)
        logger.exception("Erro na comunicação com o bacula")


def update_pool_file(procedure):
    """Pool update pool bacula file""" 
    name = procedure.pool_bacula_name()
    filename = path.join(settings.NIMBUS_POOLS_DIR, name)
    render_to_file(filename, "pool", name=name, max_vol_bytes=procedure.pool_size,
                   days=procedure.pool_retention_time)

def remove_pool_file(procedure):
    """pool remove file"""
    name = procedure.pool_bacula_name()
    filename = path.join(settings.NIMBUS_POOLS_DIR, name)
    utils.remove_or_leave(filename)

#signals.connect_on(update_pool_file, Procedure, post_save)
#signals.connect_on(remove_pool_file, Procedure, post_delete)

signals.connect_on( update_procedure_file, Procedure, post_save)
signals.connect_on( remove_procedure_volumes, Procedure, post_delete)
signals.connect_on( remove_procedure_file, Procedure, post_delete)

