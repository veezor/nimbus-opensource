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



import unittest

import os
import pdb
import sys
import shutil



import keymanager

class KeyManagerTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.password = "1234"
        self.drive = "/tmp/strongbox.crypto"
        self.mountpoint = "/tmp/strongbox"
        self.backupfile = "/tmp/strongbox.crypto.backup"
        self.new_password = "4567"
        self.keymanager = keymanager.KeyManager( password = self.password,
                                                 drive = self.drive,
                                                 mountpoint = self.mountpoint )
        


    def test_01_create(self):

        km = keymanager.KeyManager( password = self.password,
                                                 drive = self.drive,
                                                 mountpoint = self.mountpoint )
        self.assertEqual( self.password, km.password )
        self.assertEqual( self.drive, km.drive )
        self.assertEqual( self.mountpoint, km.mountpoint )
        self.assertFalse( km.mounted )


    def test_02_set_password(self):
        password = "4567"
        self.keymanager.set_password(password)
        self.assertEqual( self.keymanager.password, password )
        self.keymanager.set_password(self.password)

    def test_04_mount_drive(self):
        r = self.keymanager.mount_drive()
        self.assertTrue( r )
        self.assertTrue( self.keymanager.mounted )

    def test_03_create_drive(self):
        try:
            shutil.rmtree(self.keymanager.drive)
        except OSError, error:
            print error
            pass
        r = self.keymanager.create_drive()
        self.assertTrue( r )

    def test_05_umount_drive(self):
        r = self.keymanager.umount_drive()
        self.assertTrue( r )
        self.assertFalse( self.keymanager.mounted )

    def test_07_force_umount_drive(self):
        r = self.keymanager.force_umount_drive()
        self.assertTrue( r )
        self.assertFalse( self.keymanager.mounted )

    def test_06_generate_and_save_keys(self):
        r = self.keymanager.generate_and_save_keys_for_client('test')
        self.assertTrue( r )

    def test_08_has_drive(self):
        try:
            r = self.keymanager.has_drive()
            self.assertTrue( r )
        except IOError, e:
            pass

    def test_09_make_backup(self):
        r = self.keymanager.make_drive_backup(self.backupfile)
        self.assertTrue(r)

    def test_10_restore_backup(self):
        r = self.keymanager.restore_drive_backup(self.backupfile)
        self.assertTrue(r)

    def test_11_change_drive_password(self):
        r = self.keymanager.change_drive_password( self.new_password )
        self.password = self.new_password
        self.test_04_mount_drive()
        self.test_07_force_umount_drive()
        self.assertTrue(r)







if __name__ == "__main__":
    unittest.main()

