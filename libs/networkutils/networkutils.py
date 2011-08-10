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
