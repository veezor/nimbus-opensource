#!/usr/bin/python

import subprocess
import os
import hashlib
import shutil
import math
import re
import time
import cPickle


from encryptdevicemanager import exceptions as exc
from encryptdevicemanager.backends.base import IEncryptDeviceManager


# CRYPTDIR is the folder containing encrypted data.
# It is located at ~/.Crypt if in $HOME
# or /mount-point/.Crypt-user (like Trash).
MTAB = "/etc/mtab"
FUSERMOUNT = "/bin/fusermount"
ENCFS = "/usr/bin/encfs"
ENCFSCTL = "/usr/bin/encfsctl"
MOUNT = "/bin/mount"
# n for normal mode, p for paranoia mode
MODE = "p"
KEYFILE = ".encfs6.xml"
ECHO = "/bin/echo"



class Encfs(IEncryptDeviceManager):
    """Encfs wrapper"""


    def __init__(self, device, mountpoint):
        super(Encfs, self).__init__( device, mountpoint)


    def change_password(self, old, new):
        """Change password"""
        param = "%(old)s\n%(new)s\n" % {"old": old, "new" : new}
        p1 = subprocess.Popen([ECHO, "-e", param],\
            stdout=subprocess.PIPE)
        p2 = subprocess.Popen([ENCFSCTL, "autopasswd", self.device],\
            stdin=p1.stdout, stdout=subprocess.PIPE)
        p2.communicate()[0]
        
        if p2.returncode is not 0:
            raise exc.BadPassword()

        return (not bool(p2.returncode))


    def create(self, password):
        """Encrypt a folder"""
        
        if len(password) == 0:
            raise exc.NullPassword()

        if os.path.exists( os.path.join(self.device, KEYFILE) ):
            print self.device
            raise exc.AlreadyExists()


        if not os.path.exists(self.mountpoint):
            os.makedirs(self.mountpoint)

        os.makedirs(self.device)

        param = "%(mode)s\n%(pass)s\n" % {"mode": MODE, "pass": password}
        p1 = subprocess.Popen([ECHO, "-e", param], stdout=subprocess.PIPE)
        p2 = subprocess.Popen([ENCFS, "-S", self.device,\
            self.mountpoint], stdin=p1.stdout, stdout=subprocess.PIPE)
        p2.communicate(param)[0]
        if p2.returncode is not 0:
            raise exc.BadPassword()

        self.umount()

        return (not bool(p2.returncode))


    def mount(self, password, idle=None):
        """Mount an encrypted folder"""

        if self.is_mounted():
            return

        p1 = subprocess.Popen([ECHO, password],\
            stdout=subprocess.PIPE)
        if idle == None:
            p2 = subprocess.Popen([ENCFS, "-S", self.device,\
                self.mountpoint, "--", "-o", "nonempty"],\
                    stdin=p1.stdout, stdout=subprocess.PIPE)
        else:
            p2 = subprocess.Popen([ENCFS, "-S", self.device, "-i",\
                str(idle), self.mountpoint, "--", "-o", "nonempty"],\
                    stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = p2.communicate(password + "\n")[0]
        if p2.returncode is not 0:
            raise exc.BadPassword()


        return (not bool(p2.returncode))

    def umount(self):
        """Unmount an encrypted folder"""
        p = subprocess.Popen([FUSERMOUNT, "-z", "-u", self.mountpoint])
        p.communicate()
        return (not bool(p.returncode))


    def umountf(self):
        return self.umount()

    def make_backup(self, password, target):
        shutil.copyfile(  os.path.join(self.device, KEYFILE), target )
        return True

    def restore_backup(self, password, backup):
        shutil.copyfile( backup, os.path.join(self.device, KEYFILE) )
        return True

    def is_mounted(self):
        """Test if a folder is mounted"""
        p = subprocess.Popen([MOUNT], stdout=subprocess.PIPE)
        p = p.communicate()[0]
        p = p.split("\n")
        
        r = re.compile("^encfs on %s type fuse" % self.mountpoint)
        for l in p:
            if r.match(l):
                return True
        return False

