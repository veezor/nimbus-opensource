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




import subprocess
from os.path import join


BACULA_ROOT = "/usr/bin/"
BACULA_DIR = join(BACULA_ROOT, "bacula-dir")
BACULA_SD = join(BACULA_ROOT, "bacula-sd")
BACULA_FD = join(BACULA_ROOT, "bacula-fd")
BCONSOLE = join(BACULA_ROOT, "bconsole")


class ConfigFileError(Exception):
    pass


def _call_test_command(binary, filename):
    try:
        popen = subprocess.Popen( [binary, "-t", "-c",filename],
                                  stdout=subprocess.PIPE)
        popen.wait()
    except OSError, error:
        raise ConfigFileError(error)

    if popen.returncode != 0:
        raise ConfigFileError(popen.stdout.read())

    return popen.returncode


def check_bconsole(filename):
    return _call_test_command(BCONSOLE, filename)


def check_baculadir(filename):
    return _call_test_command(BACULA_DIR, filename)

 
def check_baculafd(filename):
    return _call_test_command(BACULA_FD, filename)


def check_baculasd(filename):
    return _call_test_command(BACULA_SD, filename)
