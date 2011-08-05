#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class NotImplemented(object):
    pass

class IEncryptDeviceManager(object):

    __register = set()
    __active = None


    def __init__(self, device, mountpoint, *args, **kwargs):
        self.device = device
        self.mountpoint = mountpoint
        self.register(self)

    def mount(self, password):
        pass

    def umount(self):
        pass

    def umountf(self):
        pass

    def create(self, password):
        pass

    def make_backup(self, password, target):
        pass

    def restore_backup(self, password, backup):
        pass

    def change_password(self, old, new):
        pass


    @classmethod
    def register(cls, manager):
        cls.__register.add(manager.__class__)


    @classmethod
    def install(cls, manager=None):
        if not manager:
            manager = cls
        IEncryptDeviceManager.__active = manager

    @classmethod
    def get_active_backend(cls):
        return cls.__active

    @classmethod
    def get_available_backends(cls):
        return list( cls.__register.union( set(cls.__subclasses__()) ) )



