#!/usr/bin/env python
# -*- coding: UTF-8 -*-


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


