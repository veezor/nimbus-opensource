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


from cx_Freeze import setup, Executable



import sys
import os
from os.path import join, dirname, walk, exists


sys.path.append( join( dirname(__file__), '..'))
sys.path.append( join( dirname(__file__), '..', 'libs'))

from nimbus import settings

packages = [ "pybacula",
             "networkutils",
             "keymanager",
             "encryptdevicemanager",
             "nimbus",
             "nimbus.settings",
             "nimbus.shared",
             "nimbus.libs"]



def has_templates(name):
    appname = name.split('.')[-1]
    template_dir = join(appname, 'templates')
    return exists(template_dir)

def get_template_dir(name):
    nimbus, appname = name.split('.')
    fdir = join(appname, 'templates')
    fulldir = join(nimbus, appname, 'templates')
    return fdir, fulldir


nimbus_apps = [  app for app in settings.INSTALLED_APPS if app.startswith('nimbus') ]
packages.extend( nimbus_apps )
templates_dir = [ get_template_dir(app) for app in nimbus_apps if has_templates(app) ]


setup(
        name = "Nimbus",
        version = "1.0",
        description = "Nimbus Cloud Backup",
        executables = [ Executable("main.py", targetName="nimbus")],
        options = { "build_exe":
                      { "compressed" :  True,
                        "build_exe" : "binary",
                        "silent" : True,
                        "optimize" :  "1",
                        "create_shared_zip" :  False,
                        "include_in_shared_zip" : False,
                        "append_script_to_exe" :  True,
                        "packages": packages,
                        "excludes" : ["email","PIL","django", "xml", "pytz", "gunicorn", "distutils", "json"],
                        "zip_includes" : templates_dir,
                        "include_files" : [ ("media", "media" )],
                      }
        }
)
