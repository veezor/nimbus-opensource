#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import subprocess
import logging


from encryptdevicemanager import exceptions as exc
from encryptdevicemanager.backends.base import IEncryptDeviceManager


TRUECRYPT_EXEC = "/usr/bin/truecrypt"



COMMANDS = {
        "create" : """truecrypt -t -c --volume-type=Normal --size=1572864 --encryption=AES-Twofish-Serpent --hash=Whirlpool --filesystem=FAT --password=%s --keyfiles= --random-source=/dev/urandom %s""",
        "mount" : """sudo truecrypt -t --password=%s --keyfiles= --protect-hidden=no %s %s""",
        "umount" : """sudo truecrypt -t -d %s""",
        "umountf" : """sudo truecrypt -t -d -f %s""",
        "changepassword" : """truecrypt -t -C --password=%s --keyfiles= --new-keyfiles= --new-password=%s --random-source=/dev/urandom %s""",
        "backup": """truecrypt  -t --backup-headers --random-source=/dev/urandom  %s""",
        "restore" : """truecrypt -t --restore-headers  --random-source=/dev/urandom %s""",
        "is_mounted" : """truecrypt -t -l""" 
}






def has_truecrypt():
    return os.access( TRUECRYPT_EXEC, os.X_OK )



class TrueCrypt(IEncryptDeviceManager):

    _MAKE_BACKUP_PARAMS = "%(password)s\n\nn\ny\n%(target)s\n"      # 1 - password
                                                                    # 2 - keyfiles
                                                                    # 3 - contain hidden volumes
                                                                    # 4 - want to create volume header backup
                                                                    # 5 - dest filename

    _RESTORE_BACKUP_PARAMS = "2\ny\n%(backup)s\n%(password)s\n\n"   # 1 - external backup
                                                                    # 2 - you want to restore volume header
                                                                    # 3 - backup filename 
                                                                    # 4 - password of backup
                                                                    # 5 - keyfiles

    def __init__(self, device, mountpoint):
        super(TrueCrypt, self).__init__( device, mountpoint )
        if not has_truecrypt():
            raise exc.SystemExecutableNotFound("TrueCrypt executable not found")

    def _get_popen(self, cmd):
        return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr = subprocess.PIPE )

    def _generate_list(self, cmd, *args):
        cmd = COMMANDS[cmd].split()
        index = 0
        for i,param in enumerate(cmd):
            if "%s" in param:
                cmd[i] = cmd[i] % args[index]
                index += 1
        return cmd

    def call_command(self, cmd, params=None, input=None):
        cmd = self._generate_list( cmd, *params)
        p = self._get_popen(cmd)
        stdout, stderr = p.communicate(input)
        try:
            logger = logging.getLogger(__name__)
            msg = "Executando o comando: %s\nStdout: %s\nStderr: %s\nReturn code: %s"
            logger.info( msg % (" ".join(cmd),stdout,stderr,p.returncode ))
        except Exception, e:
            logger.exception("Erro ao fazer log de comando do truecrypt")
        return (not bool(p.returncode)),stdout,stderr


    def create(self, password):
        return self.call_command( "create", params=(password, self.device))[0]


    def mount(self, password):

        ok, stdout, stderr = self.call_command( "mount", 
                                                params=(password, 
                                                        self.device, self.mountpoint))
        if stdout.startswith("Incorrect password"):
            raise exc.BadPassword("Incorrect password")
        return ok


    def umount(self):
        return self.call_command( "umount", params=(self.mountpoint,))[0]



    def umountf(self):
        return self.call_command( "umountf", params=(self.mountpoint,))[0]



    def change_password(self, oldpassword, newpassword):
        return self.call_command( "changepassword", 
                                  params=(oldpassword, newpassword, self.device))[0]



    def make_backup(self, password, target):
        ok, stdout, stderr = self.call_command( "backup", params=(self.device,),
                                 input = self._MAKE_BACKUP_PARAMS % locals())

        if "Incorrect password" in stdout:
            raise exc.BadPassword("Incorrect password")
        return ok



    def restore_backup(self, password, backup):
        ok, stdout, stderr = self.call_command( "restore", params=(self.device,),
                                 input = self._RESTORE_BACKUP_PARAMS % locals())
        if "Incorrect password" in stderr:
            raise exc.BadPassword("Incorrect password")
        return ok


    def is_mounted(self):
        ok, stdout, stderr = self.call_command( "is_mounted", 
                                                params=(self.device,)) 
        if ok == True and self.device in stdout:
            return True
        return False


