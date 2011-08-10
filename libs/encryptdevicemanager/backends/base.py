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




class NotImplemented(object):
    pass

class IEncryptDeviceManager(object):

    __register = set()
    __active = None


    def __init__(self, device, mountpoint, *args, **kwargs):
        self.device = device
        self.mountpoint = mountpoint
        self.register(self)

    def mount(self, password):
        pass

    def umount(self):
        pass

    def umountf(self):
        pass

    def create(self, password):
        pass

    def make_backup(self, password, target):
        pass

    def restore_backup(self, password, backup):
        pass

    def change_password(self, old, new):
        pass


    @classmethod
    def register(cls, manager):
        cls.__register.add(manager.__class__)


    @classmethod
    def install(cls, manager=None):
        if not manager:
            manager = cls
        IEncryptDeviceManager.__active = manager

    @classmethod
    def get_active_backend(cls):
        return cls.__active

    @classmethod
    def get_available_backends(cls):
        return list( cls.__register.union( set(cls.__subclasses__()) ) )



