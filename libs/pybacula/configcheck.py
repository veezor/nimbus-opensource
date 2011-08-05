#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import subprocess
from os.path import join


BACULA_ROOT = "/usr/bin/"
BACULA_DIR = join(BACULA_ROOT, "bacula-dir")
BACULA_SD = join(BACULA_ROOT, "bacula-sd")
BACULA_FD = join(BACULA_ROOT, "bacula-fd")
BCONSOLE = join(BACULA_ROOT, "bconsole")


class ConfigFileError(Exception):
    pass


def _call_test_command(binary, filename):
    try:
        popen = subprocess.Popen( [binary, "-t", "-c",filename],
                                  stdout=subprocess.PIPE)
        popen.wait()
    except OSError, error:
        raise ConfigFileError(error)

    if popen.returncode != 0:
        raise ConfigFileError(popen.stdout.read())

    return popen.returncode


def check_bconsole(filename):
    return _call_test_command(BCONSOLE, filename)


def check_baculadir(filename):
    return _call_test_command(BACULA_DIR, filename)

 
def check_baculafd(filename):
    return _call_test_command(BACULA_FD, filename)


def check_baculasd(filename):
    return _call_test_command(BACULA_SD, filename)
