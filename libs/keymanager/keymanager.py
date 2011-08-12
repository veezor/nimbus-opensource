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
from os.path import join
import subprocess
import tempfile

import encryptdevicemanager as EncDeviceManager


ENCRYPT_DEVICE = "/var/nimbus/strongbox.crypto"
MOUNTPOINT = "/media/strongbox"



def generate_pem(key, certificate):
    return key + certificate



def generate_key(filename):
    cmd = subprocess.Popen(["openssl", "genrsa", "-out", filename, "2048", "-days","3650"],
                           stdout=subprocess.PIPE)
    cmd.communicate()

    with file(filename) as f:
        content = f.read()

    return content



def generate_certificate(keyfilename, filename, sslconfig):
    cmd = subprocess.Popen(["openssl", "req", "-new", 
                            "-key", keyfilename, "-x509",
                            "-config", sslconfig,
                            "-days","3650",
                            "-out", filename],
                            stdout=subprocess.PIPE)
    cmd.communicate()

    with file(filename) as f:
        content = f.read()

    return content



def generate_all_keys(sslconfig, prefix=None):

    if prefix:
        keyfilename = join(prefix,  "client.key")
        certfilename = join(prefix,  "client.cert")
    else:
        keyfilename = tempfile.mktemp()
        certfilename = tempfile.mktemp()

    key = generate_key(keyfilename)
    cert = generate_certificate(keyfilename, certfilename, sslconfig)
    pem = generate_pem(key, cert)

    return key, cert, pem




class KeyManager(object):

    def __init__(self, password=None, drive=ENCRYPT_DEVICE, 
                                      mountpoint=MOUNTPOINT):
        self.drive = drive
        self.password = password
        self.mountpoint = mountpoint
        self.devmanager = EncDeviceManager.Manager(self.drive, 
                                                   self.mountpoint)

    @property
    def mounted(self):
        return self.devmanager.is_mounted()

    def set_password(self, password):
        self.password = password

    def has_drive(self):
        return os.access(self.drive, os.R_OK)

    def create_drive(self):
        return self.devmanager.create(self.password)

    def get_client_path(self, client):
        return os.path.join( self.mountpoint, client )

    def get_client_path_file(self, client, path):
        return os.path.join( self.mountpoint, client, path)

    def generate_and_save_keys_for_client(self, client):
        self.mount_drive()
        dirpath = self.get_client_path(client)
        if not os.access(dirpath, os.W_OK):
            os.mkdir(dirpath)
        return generate_and_save_keys(dirpath)


    def mount_drive(self):

        if not os.access(self.mountpoint, os.W_OK):
            #os.mkdir(self.mountpoint)
            pass

        if not self.mounted:
            return self.devmanager.mount( self.password )
        return False


    def umount_drive(self, force=False):
        if force:
            return self.force_umount_drive()
        return self.devmanager.umount()

    
    def force_umount_drive(self):
        return self.devmanager.umountf()


    def change_drive_password(self, new_password):
        r = self.devmanager.change_password(self.password, 
                                           new_password)

        self.set_password( new_password )
        return r

    def make_drive_backup(self, backupfilename):
        return self.devmanager.make_backup( self.password, 
                                           backupfilename)

    def restore_drive_backup(self, backupfilename):
        return self.devmanager.restore_backup( self.password, 
                                               backupfilename)

    def remove_backup_file(self, backupfilename):
        return os.remove( backupfilename )
