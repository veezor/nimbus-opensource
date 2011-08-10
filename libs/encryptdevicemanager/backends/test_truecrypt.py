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

from encryptdevicemanager.backends import truecrypt
from encryptdevicemanager.backends.truecrypt import TrueCrypt
from encryptdevicemanager import exceptions as exc



class TrueCryptTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filedrive = "/tmp/drive.crypto"
        self.mountpoint = "/tmp/drivetest"
        self.truecrypt = TrueCrypt(self.filedrive, 
                                   self.mountpoint)
        self.password = '1234'
        self.new_password = "4567"
        self.fileback = '/tmp/drive.crypto.back'

    def test_1_create_drive(self):
        r = self.truecrypt.create(self.password)
        self.assertTrue(r)

    def test_get_popen(self):
        popen = self.truecrypt._get_popen(["echo","test"])
        stdout, stdin = popen.communicate()
        self.assertEqual( stdout, 'test\n')
    
    def test_generate_list(self):
        genlist = self.truecrypt._generate_list("create", self.password, self.filedrive)
        cmd = " ".join(genlist)

        self.assertEqual( cmd,
                         truecrypt.COMMANDS['create'] % ( self.password,
                                                          self.filedrive))



    def test_2_1_mount_drive(self):

        try:
            os.mkdir(self.mountpoint)
        except OSError, e:
            pass #silent file exists
        

        r = self.truecrypt.mount(self.password)
        self.assertTrue(r)

    def test_2_2_is_mounted(self):
        r = self.truecrypt.is_mounted()
        self.assertTrue(r)


    def test_3_umount_drive(self):
        r = self.truecrypt.umount( )
        self.assertTrue(r)

    def test_6_umountf_drive(self):
        self.test_2_1_mount_drive()
        r = self.truecrypt.umountf( )
        self.assertTrue(r)

    def test_4_make_backup(self):
        r = self.truecrypt.make_backup(self.password, self.fileback)
        self.assertTrue(r)


    def test_5_restore_backup(self):
        r = self.truecrypt.restore_backup(self.password, self.fileback)
        self.assertTrue(r)

    def test_7_password_error(self):
        self.password = "error"
        self.assertRaises( exc.BadPassword, self.truecrypt.mount,
                           self.password )
        self.assertRaises( exc.BadPassword, self.truecrypt.make_backup,
                           self.password, self.fileback)
        self.assertRaises( exc.BadPassword, self.truecrypt.restore_backup,
                           self.password, self.fileback)


    def test_8_change_drive_password(self):
        r = self.truecrypt.change_password( self.password, 
                                            self.new_password)
        self.password = self.new_password
        self.test_2_1_mount_drive()
        self.assertTrue(r)



if __name__ == "__main__":
    unittest.main()

