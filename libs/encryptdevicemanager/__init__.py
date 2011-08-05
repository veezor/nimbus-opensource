#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from encryptdevicemanager.backends import IEncryptDeviceManager
from encryptdevicemanager.manager import ( Manager,
                                           install, 
                                           register, 
                                           get_available_backends,
                                           get_active_backend )
