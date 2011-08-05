#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class AlreadyEncrypted(Exception):
    def __str__(self):
        return "This is already a crypted folder"



class SystemExecutableNotFound(Exception):
    def __str__(self):
        return "A system executable required is missing"


class BadPassword(Exception):
    def __str__(self):
        return "The password is wrong"


class NullPassword(Exception):
    def __str__(self):
        return "Password can not be null"


class AlreadyExists(Exception):
    def __str__(self):
        return "This folder already exists"


class AlreadyOpened(Exception):
    def __str__(self):
            return "This folder is already opened"


class NoEncrypted(Exception):
    def __str__(self):
            return "This folder is not crypted"


class NotOpened(Exception):
    def __str__(self):
            return "This folder is not opened"
     
           
class LoError(Exception):
    def __str__(self):
            return "No loopback device available"


class NotDir(Exception):
    def __str__(self):
            return "This is not a folder"


