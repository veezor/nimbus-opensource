#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import time
import logging
import logging.config
import shutil
import ConfigParser
import signal

NIMBUS_MANAGER_CONF = "/etc/nimbus/nimbus_manager.conf"
NIMBUS_LOGGING_CONF = "/etc/nimbus/nimbus_manager_log.conf"

class FileNotFound(Exception):
    pass




def has_config():
    return os.access(NIMBUS_MANAGER_CONF, os.R_OK)


def load_logging_system():
    logging.config.fileConfig(NIMBUS_LOGGING_CONF)


def load_config():
    if has_config():
        config = ConfigParser.ConfigParser()
        config.read(NIMBUS_MANAGER_CONF)
        return config
    else:
        logger = logging.getLogger(__name__)
        logger.error("Arquivo de configuração do nimbusmanager ausente!")
        raise FileNotFound("Arquivo de configuração do nimbusmanager ausente!")
    return None



def get_config():
    if not get_config.memo:
        get_config.memo = load_config()
    return get_config.memo
get_config.memo = None



def make_backup(filename):
    logger = logging.getLogger(__name__)
    logger.info("Arquivo de backup criado para %s." % filename)
    try:
        shutil.copy(filename, filename + ".nimbus-bkp")
    except IOError, e:
        pass


def kill_older_manager():
    try: 
        config = get_config()
        pidfile = config.get("PATH","pid")
        pid = file(pidfile).read()
        pid = int(pid)
        logger.warning("Enviando SIGKILL ao daemon")
        os.kill(pid, signal.SIGKILL)
    except (ValueError, IOError), e:
        logger.warning("Arquivo de pid vazio")
    except OSError, e:
        logger.info("Nenhum manager rodando")

def current_time(uct=False):
    if uct:
        time_function = time.gmtime
    else:
        time_function = time.localtime
    return time.strftime("%d-%m-%Y %H:%M:%S", time_function())
