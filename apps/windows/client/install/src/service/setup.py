#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup
import py2exe

class Target(object):
    def __init__(self,**kw):
        self.__dict__.update(kw)

service = Target(modules=['winservice'],
                 cmdline_style='pywin32')

setup(name='NimbusService',
      version='1.0',
      author='veezor',
      service=[service],
      zipfile=None,
      options={ 'py2exe' : 
                { 'bundle_files' : 1,
                }
})
