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


#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time
import string
from random import choice
from itertools import izip

from django.conf import settings
from django.contrib import messages

class Referer(object):
    def __init__(self, request):
        self.raw = request.META.get('HTTP_REFERER')
        if self.raw:
            self.local = self.local_address()
        else:
            self.local = ''
    
    def local_address(self):
        if self.raw.startswith('http://'):
            return '/' + '/'.join(self.raw.replace('http://','').split('/')[1:])
    

def filesizeformat(bytes, unit=""):
    
    bytes = float(bytes)
    KB = 1024
    MB = 1024*KB
    GB = 1024*MB
    TB = 1024*GB
    if unit:
        if unit == "B":
            return "%.2f bytes" % bytes
        elif unit == "KB":
            return "%.2f Kb" % (bytes/KB)
        elif unit == "MB":
            return "%.2f Mb" % (bytes/MB)
        elif unit == "GB":
            return "%.2f Gb" % (bytes/GB)
        elif unit == "TB":
            return "%.2f Tb" % (bytes/TB)
        else:
            return bytes
    else:
        if bytes < KB:
            return "%.2f bytes" % bytes
        elif bytes < MB:
            return "%.2f Kb" % (bytes/KB)
        elif bytes < GB:
            return "%.2f Mb" % (bytes/MB)
        elif bytes < TB:
            return "%.2f Gb" % (bytes/GB)
        else:
            return "%.2f Tb" % (bytes/TB)



def int_or_string(value):
    try:
        return int(value)
    except ValueError, error:
        return value

    
def dict_from_querydict(querydict, lists=()):
    d = {}
    for key, value in querydict.items():
        newkey = key.replace(".","_")

        if not newkey in lists:
            newvalue = int_or_string(value)
        else:
            newvalue = querydict.getlist(key)
            newvalue = [ int_or_string(x) for x in newvalue ]
        
        d[newkey] = newvalue

    return d


def ordered_dict_value_to_formatted_float(dictionary):
    return [ ("%.2f" % v) for k,v in sorted( dictionary.items() ) ]


def bytes_to_mb(size):
    return size/1024.0/1024

def random_password(size=20):
    """Generates random password of a given size."""
    return ''.join([choice(string.letters + string.digits) for i in range(size)])
    
    



###
###   File Handling Specific Definitions
###


def remove_or_leave(filepath):
    "remove file if exists"
    try:
        os.remove(filepath)
    except os.error:
        pass


def mount_path(filename,rel_dir):
    "mount absolute dir path and filepath"
    filename = str(filename).lower()
    base_dir = absolute_dir_path(rel_dir)
    filepath = absolute_file_path(filename, rel_dir)
    return base_dir, filepath
    
    
def absolute_file_path(filename, rel_dir):
    """Return full path to a file from script file location and given directory."""
    root_dir = absolute_dir_path(rel_dir)
    return os.path.join(root_dir, filename)


def absolute_dir_path(rel_dir):
    """Return full path to a directory from script file location."""
    return os.path.join(settings.NIMBUS_CUSTOM_DIR, rel_dir)


def isdir(path):
    if path.endswith('/'):
        return True
    else:
        return False


def get_filesize_from_lstat(lstat):
    b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    val = 0
    size = lstat.split(' ')[7] # field 7
    for i,char in enumerate(size):
        r = (b64.find(char)) * (pow(64,(len(size)-i)-1))
        val += r
    return val


def project_port(request):
    return (':%s' % request.META['SERVER_PORT']) if request.META['SERVER_PORT'] else ''


def block_ie_browser(request):
    # detects browser
    browser = request.META['HTTP_USER_AGENT']
    init_message = ""
    if re.search("MSIE", browser):
        #TODO: Insert facebox message on templates
        init_message = "$(document).ready(function(){\
                        $.facebox.settings.opacity = 0.5;\
                        jQuery.facebox({ ajax : ie_error});\
                        });"
        return messages.warning(request, "Navegador incompativel com o Nimbus. Sistema testado apenas para Google Chrome e Mozilla Firefox.")
