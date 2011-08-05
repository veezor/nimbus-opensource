#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from encryptdevicemanager.backends import IEncryptDeviceManager

class Manager(object): #Proxy

    def __init__(self, device, mountpoint):
        install()
        cls = get_active_backend()
        self.manager = cls(device, mountpoint)

    def __getattr__(self, attr_name):
        return getattr(self.manager, attr_name)


def register(manager):
    IEncryptDeviceManager.register(manager)


def get_available_backends():
    return IEncryptDeviceManager.get_available_backends()


def install(manager=None):
    if not manager:
        manager = get_available_backends()[0]
    IEncryptDeviceManager.install(manager) 


def get_active_backend():
    return IEncryptDeviceManager.get_active_backend()



