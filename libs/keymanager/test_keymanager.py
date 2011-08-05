#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

