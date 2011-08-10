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



from backends import get_active_backend, BConsoleInitError





valid_commands = """autodisplay automount add cancel create delete label
                    mount prune relabel release restore run setdebug status
                    unmount update wait disable enable list llist use query reload purge
                    .bvfs_update .bvfs_lsdir .bvfs_lsfiles"""


class CommandNotFound(Exception):
    pass


class BaculaCommandLine(object):

    connected = False
    backend = None
    
    def __init__(self, config="./bconsole.conf"):
        if not self.connected:
            BaculaCommandLine.backend = get_active_backend()() # get and instantiates
            self.backend.set_configfile(config)
            try: 
                self.backend.connect()
                BaculaCommandLine.connected = True
            except Exception, e:
                BaculaCommandLine.connected = False
                raise BConsoleInitError(e)


    def __getattr__(self, name):

        if name.startswith("_"): # bacula special commands starts with dot
            name = "." + name[1:]

        if name in valid_commands:
            return Command(name)    
        else:
            raise CommandNotFound("command not found")

    def raw(self, string):
        string = string.encode("utf-8")
        return self.backend.execute_command(string)


class Command(object):

    def __init__(self, name):
        self.content = [name]

    def raw(self, string):
        self.content.append(string)
        return self

    def __getattr__(self, attr):
        content = object.__getattribute__(self, "content")
        content.append(attr)
        return self


    def get_content(self):
        return  " ".join(self.content)

    def run(self):
        if not BaculaCommandLine.connected:
            return False
        txt = self.get_content()
        txt = txt.encode("utf-8")
        result = BaculaCommandLine.backend.execute_command( txt )
        self.content = []
        return result

    def __call__(self,*args):
        return self.run()

    def __getitem__(self, item):
        name = self.content[-1]
        self.content[-1] = ('%s="%s"' % (name,item))
        return self





