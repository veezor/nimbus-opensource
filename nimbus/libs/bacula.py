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


#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import socket
import logging
import datetime
import tempfile
import xmlrpclib
import subprocess
import SimpleXMLRPCServer
from threading import Thread

from django.conf import settings

import pybacula
from pybacula import BaculaCommandLine, configcheck, BConsoleInitError


from nimbus.shared import utils
from nimbus.bacula import models
#from nimbus.config.models import BaculaSettings


try:
    if settings.PYBACULA_TEST:
        pybacula.install_test_backend()
except AttributeError, e:
    # TODO: Tratar
    pass


class Bacula(object):

    def __init__(self):
        self.cmd = BaculaCommandLine(config=settings.BCONSOLE_CONF)
        self.logger = logging.getLogger(__name__)

    def reload(self):
        if not bacula_is_locked():
            try:
                configcheck.check_baculadir(settings.BACULADIR_CONF)
                configcheck.check_bconsole(settings.BCONSOLE_CONF)
                output = self.cmd.reload.run()
                return output
            except configcheck.ConfigFileError, error:
                logger = logging.getLogger(__name__)
                logger.exception("Arquivo de configuracao do bacula-dir gerado com erros")

    def _get_items_from_bconsole_output(self, output):
        result = []
        for line in output.split("\n"):
            data = line.split("\t")
            if len(data) > 1:
                result.append(data[-1])
        result.sort()
        return result

    def list_files(self, jobid, path):
        result = []
        self.cmd._bvfs_update.run()
        dirs = self.cmd._bvfs_lsdir.jobid[jobid].path[path].run()
        dirs = self._get_items_from_bconsole_output(dirs)
        if '.' in dirs:
            dirs.remove('.')
        if '..' in dirs:
            dirs.remove('..')
        result.extend( dirs )
        files = self.cmd._bvfs_lsfiles.jobid[jobid].path[path].run()
        result.extend( self._get_items_from_bconsole_output(files) )
        result.sort()
        result = [ path + p for p in result ]
        return result

    def run_restore(self, client_name, jobid, where, files):
        self.logger.info("Executando run_restore_")
        filename = tempfile.mktemp()
        for fname in list(files):
            if utils.isdir(fname):
                subfiles = models.File.objects\
                        .select_related()\
                        .filter(path__path__startswith=fname)
                files.extend( s.fullname for s in subfiles  )
        with file(filename, "w") as f:
            for fname in files:
                f.write( fname + "\n" )
        return self.cmd.restore.\
                client[client_name].\
                file["<" + filename].\
                restoreclient[client_name].\
                select.all.done.yes.where[where].jobid[jobid].run()

    def run_backup(self, job_name, client_name):
        """ Date Format:  YYYY-MM-DD HH:MM:SS
            Level: Full/Incremental"""
        self.logger.info("Executando run_backup ")
        sum_seconds = datetime.timedelta(seconds=10)
        now = datetime.datetime.now() + sum_seconds
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        if client_name:
            return self.cmd.run.client[client_name].\
            job[job_name].level["Full"].when[date].yes.run()


    def cancel_procedure(self, procedure):
        self.cmd.cancel.job[procedure.bacula_name].run()
        for job_id in procedure.jobs_id_to_cancel:
            self.cmd.cancel.jobid[job_id].run()


    def purge_volumes(self, volumes, pool_name):
        purge = self.cmd.purge
        for volume in volumes:
            purge.volume[volume]
        purge.pool[pool_name]
        purge.run()

    def truncate_volumes(self, pool_name):
        self.cmd.purge.volume\
            .action["truncate"]\
            .pool[pool_name].run()

    def delete_pool(self, pool_name):
        self.cmd.delete.pool[pool_name].raw('\nyes').run()


def bacula_is_locked():
    return os.path.exists(settings.BACULA_LOCK_FILE)



def unlock_bacula_and_start():
    if bacula_is_locked():
        force_unlock_bacula_and_start()


def force_unlock_bacula_and_start():
    try:
        os.remove(settings.BACULA_LOCK_FILE)
    except OSError:
        pass #ignore
    try:
        logger = logging.getLogger(__name__)
        manager = xmlrpclib.ServerProxy(settings.NIMBUS_MANAGER_URL)
        stdout = manager.director_start()
        logger.info("bacula-dir started and unlocked")
        logger.info(stdout)
    except Exception, error:
        logger.exception("start bacula-dir error")




def lock_and_stop_bacula():
    if not bacula_is_locked():
        with file(settings.BACULA_LOCK_FILE, "w"):
            pass
        logger = logging.getLogger(__name__)
        try:
            manager = xmlrpclib.ServerProxy(settings.NIMBUS_MANAGER_URL)
            stdout = manager.director_stop()
            logger.info("bacula-dir stopped and locked")
            logger.info(stdout)
        except Exception, error:
            logger.exception("stop bacula-dir error")


class BaculaLock(object):

    def __enter__(self):
        lock_and_stop_bacula()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unlock_bacula_and_start()



class ReloadManagerService(object):

    def __init__(self):
        from nimbus.config.models import BaculaSettings
        self.conf = BaculaSettings.get_instance()
        logging.config.fileConfig(settings.RELOAD_MANAGER_LOGGING_CONF)


    def add_reload_request(self):
        self.conf.increment_reload_requests_counter()

        if self.conf.reload_requests_counter > self.conf.reload_requests_threshold\
           and self._interval > self._min_interval:
            self._reload()

        return True


    def _reload(self):
        self.conf.reset_reload_requests_counter()
        self._call_reload_baculadir()


    def force_reload(self):
        self._reload()
        return True


    @property
    def _min_interval(self):
        return datetime.timedelta(seconds=self.conf.min_reload_requests_interval)

    @property
    def _interval(self):

        if not self.conf.last_bacula_reload:
            return self._min_interval + 1

        now = datetime.datetime.now()
        return now - self.conf.last_bacula_reload


    def _force_baculadir_restart(self):
        if not bacula_is_locked():
            try:
                logger = logging.getLogger(__name__)
                manager = xmlrpclib.ServerProxy(settings.NIMBUS_MANAGER_URL)
                stdout = manager.director_restart()
                logger.info("bacula-dir restart ok")
                logger.info(stdout)
            except Exception, error:
                logger.error("Reload bacula-dir error")



    def _call_reload_baculadir(self):
        try:
            logger = logging.getLogger(__name__)
            logger.info("Iniciando comunicacao com o bacula")
            bacula = Bacula()
            bacula.reload()
            logger.info("Reload no bacula executado com sucesso")
            del bacula
        except BConsoleInitError, e:
            logger.error("Comunicação com o bacula falhou, vou tentar o restart")
            self._force_baculadir_restart()
            logger.error("Comunicação com o bacula falhou")



    def run(self):
        self.thread = Thread(name='ReloadManagerService Worker',
                             target=self._start_timed_worker)
        self.thread.start()
        self._start_xmlrpc_service()


    def check_service(self):
        return True


    def _start_timed_worker(self):

        while True:
            time.sleep(self.conf.min_reload_requests_interval * 2)
            if self.conf.has_bacula_reload_requests:
                self._reload()



    def _start_xmlrpc_service(self):
        self.server = SimpleXMLRPCServer.SimpleXMLRPCServer((settings.RELOAD_MANAGER_ADDRESS,
                                                        settings.RELOAD_MANAGER_PORT))
        self.server.register_instance(self)
        self.server.serve_forever()





class ReloadManager(object):

    def __init__(self):
        self._connection = self._get_connection()


    def _get_proxy(self):
        proxy = xmlrpclib.ServerProxy(settings.RELOAD_MANAGER_URL)
        proxy.check_service()
        return proxy


    def _get_connection(self):
        try:
            return self._get_proxy()
        except socket.error:
            service = subprocess.Popen(settings.RELOAD_MANAGER_COMMAND,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            time.sleep(settings.RELOAD_MANAGER_START_SLEEP_TIME)
            return self._get_proxy()


    def add_reload_request(self):
        self._connection.add_reload_request()


    def force_reload(self):
        self._connection.force_reload()
