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
import sys
import getpass
import threading # FIX KeyError


sys.path.extend( ['/var/nimbus/deps/',
                  '/var/nimbus/deps/gunicorn-0.11.1-py2.6.egg/',
                  '/usr/lib/python2.6/dist-packages',
                  '/usr/lib/python2.6/lib-dynload',
                  '/usr/lib/python2.6/'] )



os.environ['DJANGO_SETTINGS_MODULE'] = 'nimbus.settings'


from gunicorn.app.base import Application

from django.core.handlers.wsgi import WSGIHandler
from django.core.management import call_command
from django.contrib.auth.models import User
from django.conf import settings

from nimbus.libs import graphsdata
from nimbus.libs import migrations
from nimbus.shared import utils
from nimbus.libs.bacula import ( ReloadManager,
                                 ReloadManagerService,
                                 force_unlock_bacula_and_start)
from nimbus.config.models import Config
from nimbus.storages.models import Storage
from nimbus.computers.models import Computer
from nimbus.shared.middlewares import LogSetup
from nimbus.reports.models import send_email_report
from nimbus.security.models import register_administrative_nimbus_models




class NimbusApplication(Application):

    def init(self, parser, opts, args):
        self.project_path = 'nimbus'
        self.settings_modname = "nimbus.settings"
        self.cfg.set("default_proc_name", self.settings_modname)
        self.cfg.set("timeout", 2592000)


    def load(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = self.settings_modname
        return WSGIHandler()


class App(object):

    def create_database(self):
        call_command('syncdb',verbosity=0,interactive=False)
        if len(User.objects.all()) == 0:
            u = User(username = "admin",
                     is_superuser=True,
                     email = "suporte@veezor.com")
            u.set_password("admin")
            u.save()

            call_command('loaddata', settings.INITIALDATA_FILE)


            config = Config.get_instance()
            config.director_password = utils.random_password()
            config.save()

            storage = Storage.objects.get(id=1)
            storage.password =  utils.random_password()
            storage.save()

            computer = Computer.objects.get(id=1)
            computer.activate()

            register_administrative_nimbus_models()

            reload_manager = ReloadManager()
            reload_manager.force_reload()
        else:
            force_unlock_bacula_and_start()




    def update_graphs_data(self):
        graphs_data_manager = graphsdata.GraphDataManager()
        graphs_data_manager.update()


    def shell(self):
        call_command('shell')

    def run_server(self):
        NimbusApplication("%prog [OPTIONS] [SETTINGS_PATH]").run()



    def change_password(self):

        while True:
            password = getpass.getpass("new password: ")
            confirm_password = getpass.getpass("confirm password: ")

            if password != confirm_password:
                print "password does not match"
                print
            else:
                user = User.objects.get(id=1)
                user.set_password(password)
                user.save()
                print "password changed"
                break


    def reload_manager_service(self):
        service = ReloadManagerService()
        service.run()

    def send_email_report(self):
        job_id =  int(sys.argv[2])
        send_email_report(job_id)


    def update_10_to_11(self):
        try:
            migrations.update_10_to_11()
        except migrations.ComputerUpdateError:
            print "Erro: todos os clientes devem estar ativos na rede"
            sys.exit(1)

    def run(self):
        commands = {
            "--server-forever" : self.run_server,
            "--update-graphs-data" : self.update_graphs_data,
            "--create-database" : self.create_database,
            "--shell" : self.shell,
            "--change-password" : self.change_password,
            "--start-reload-manager-service" : self.reload_manager_service,
            "--email-report": self.send_email_report,
            "--update-1.0-to-1.1" : self.update_10_to_11
        }

        if len(sys.argv) > 1:
            try:
                commands[sys.argv[1]]()
            except KeyError, error:
                print "option not found:",sys.argv[1]
                sys.exit(1)
        else:
            self.run_server()




def main():
    LogSetup()
    App().run()

if __name__ == "__main__":
    main()
