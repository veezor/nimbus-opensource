#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

