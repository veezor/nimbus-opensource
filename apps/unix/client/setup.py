#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup

setup(name='Nimbus Client Service',
      version='1.0',
      description='Client for Nimbus Cloud Backup',
      author='Veezor',
      author_email='contact@veezor.com',
      license="GPL",
      url='www.nimbusbackup.com',
      data_files=[
          ('/etc/init.d', ['etc/init.d/nimbusclient']),
          ('/etc/nimbus', [])
      ],
      scripts=['usr/sbin/nimbusnotifier', 'usr/sbin/nimbusclientservice'],
     )
