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
import sys
import re
import logging
import traceback
import logging.config

from django.conf import settings
from backgroundjobs import ThreadPool as BJThreadPool






class LogSetup(object): # on bootstrap

    def __init__(self):
        logging.config.fileConfig(settings.LOGGING_CONF)
        pass



class ThreadPool(object):

    instance = None

    def __init__(self):
        if not self.instance:
            self.__class__.instance = BJThreadPool()


    @classmethod
    def get_instance(cls):
        return cls.instance




class AjaxDebug(object):

    def process_exception(self, request, exception):
        traceback.print_exc(file=sys.stderr)
        logger = logging.getLogger(__name__)
        logger.exception("Exception levantada no django")
