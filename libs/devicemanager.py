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
from subprocess import check_call, CalledProcessError



PMOUNT="/usr/bin/pmount"
PUMOUNT="/usr/bin/pumount"


class MountError(Exception):
    pass

class UmountError(Exception):
    pass


class StorageDeviceManager(object):

    def __init__(self, labelname):
        self.labelname = labelname


    def _storage_info(self):
        if self.mounted:
            info = os.statvfs(self.mountpoint)
            total = info.f_bsize * info.f_blocks
            free = info.f_bsize * info.f_bfree
            used = total - free
            return total, used, free
        else:
            return 0,0,0


    @property
    def mounted(self):
        f = file("/etc/mtab")
        content = f.read()
        f.close()
        return self.mountpoint in content

    @property
    def device(self):
        return os.path.join("/dev/disk/by-label", self.labelname)


    @property
    def mountpoint(self):
        return os.path.join("/media", self.labelname)


    @property
    def available_size(self):
        total, used, free = self._storage_info()
        return free


    @property
    def used_size(self):
        total, used, free = self._storage_info()
        return used


    @property
    def size(self):
        total, used, free = self._storage_info()
        return total


    def mount(self):
        if not self.mounted:
            try:
                r = check_call([PMOUNT, self.device, self.labelname])
            except CalledProcessError, e:
                raise MountError(e)
            if r:
                raise MountError("mount return is %d" % r)


    def umount(self):
        if self.mounted:
            try:
                r = check_call([PUMOUNT, self.labelname])
            except CalledProcessError, e:
                raise UmountError(e)
            if r:
                raise UmountError("umount return is %d" % r)


