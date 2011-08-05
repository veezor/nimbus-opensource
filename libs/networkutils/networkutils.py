#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import netifaces
from netifaces import AF_INET, AF_LINK, AF_INET6
import subprocess
import socket



class NotImplemented(Exception):
    pass

class HostAddrNotFound(Exception):
    pass

class HostNameNotFound(Exception):
    pass

class InterfaceNotFound(Exception):
    pass

class Interface(object):

    def __init__(self, name):
        self.name = name
        data = netifaces.ifaddresses(name)
        try:
            inet =  data[AF_INET][0]
            link = data[AF_LINK][0]
            self.addr = inet['addr']
            self.broadcast = inet['broadcast']
            self.netmask = inet['netmask']
            self.mac = link['addr']
        except KeyError:
            raise InterfaceNotFound()

    def __repr__(self):
        return self.__class__.__name__ + "(%s)" % (self.name)

    @staticmethod
    def from_dict(dic):
        i = Interface(dic['name'])
        vars(i).update(dic)
        return i



def get_interface(name):
    try:
        iface = Interface(name)
    except KeyError:
        raise InterfaceNotFound()
    return iface


def get_interfaces():
    interfaces = []
    for name in netifaces.interfaces():
        try:
            interface = Interface(name)
            interfaces.append(interface)
        except InterfaceNotFound:
            pass
    return interfaces


def resolve_name(name):
    try:
        return socket.gethostbyname(name)
    except socket.gaierror, e:
        raise HostNameNotFound('Host name not found')
 
 
def resolve_addr(addr):
    try:
        return socket.gethostbyaddr(addr)[0]
    except socket.herror, e:
        raise HostAddrNotFound('Host address not found')



def traceroute(host):
    cmd = subprocess.Popen( [ "/usr/bin/traceroute", 
                             str(host) ], stdout = subprocess.PIPE)
    cmd.wait()
    return cmd.returncode, cmd.stdout.read()

def ping(host, packets=10):
    cmd = subprocess.Popen( [ "/bin/ping", 
                             "-c",str(packets),
                             str(host) ], stdout = subprocess.PIPE)
    cmd.wait()
    return cmd.returncode, cmd.stdout.read()
