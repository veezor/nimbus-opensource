#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import logging
from subprocess import Popen, PIPE

try:
    import bconsole
except ImportError, e:
    bconsole = None


BCONSOLE_EXECUTABLE="bconsole"
BCONSOLE_PATH="/usr/bin"


class BConsoleInitError(Exception):
    pass

class NotImplemented(Exception):
    pass



class IConsole(object): 

    def connect(self):
        raise NotImplemented("method implementation required")

    def execute_command(self, arg):
        raise NotImplemented("method implementation required")

    def set_configfile(self, filename):
        raise NotImplemented("method implementation required")

    def close(self):
        raise NotImplemented("method implementation required")

    @classmethod
    def install(cls):
        global _active_backend
        _active_backend = cls




class MockConsole(IConsole):
     
    def connect(self):
        pass

    def execute_command(self, arg):
        pass

    def set_configfile(self, filename):
        pass

    def close(self):
        pass



class SubprocessConsole(IConsole):

    def __init__(self, configfile="./bconsole.conf"):
        self.configfile = configfile
        self.executable = BCONSOLE_EXECUTABLE
        self.bconsole_path = BCONSOLE_PATH
        self.connection = None

    def set_configfile(self, configfile):
        self.configfile = configfile

    def execute_command(self, command):
        executable = os.path.join(self.bconsole_path, self.executable)
        self.connection = Popen( [executable, "-c", self.configfile], 
                                 bufsize=0, stdin=PIPE, stdout=PIPE, stderr=PIPE)


        try:
            output, error = self.connection.communicate(command)
            self.connection.wait()
        except OSError, error:
            output = ""
            error = ""

        logging.info("Bacula command is %s", command)
        logging.info("Stdout is %s", output)
        logging.info("Stderr is %s", error)
        if self.connection.returncode != 0:
            logging.error("Error on bconsole connection")
            logging.error("Returncode is %s" % self.connection.returncode)
            logging.error(output)
            logging.error(error)
            raise BConsoleInitError("Communication failed")
        return output

    def connect(self):
        pass # not necessary

    def close(self):
        try:
            self.connection.terminate()
        except AttributeError, e:
            pass



if bconsole:


    class BindingConsole(IConsole):

        def __init__(self, configfile="./bconsole.conf"):
            bconsole.set_configfile(configfile)

        def set_configfile(self, configfile):
            bconsole.set_configfile(configfile)

        def execute_command(self, command):
            bconsole.execute_command(command)

        def connect(self):
            bconsole.connect()

        def close(self):
            bconsole.close()


    _active_backend = BindingConsole

else:            
    _active_backend = SubprocessConsole


def get_available_backends():
    return IConsole.__subclasses__()

def get_active_backend():
    return _active_backend

def install_backend(iconsole):
    if iconsole in get_available_backends():
        global _active_backend
        _active_backend = iconsole

def install_test_backend():
    global _active_backend
    _active_backend = MockConsole

