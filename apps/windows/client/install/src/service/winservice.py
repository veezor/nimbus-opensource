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



import os
import sys
import codecs
import win32serviceutil
import win32service
import win32event
import win32api
import win32evtlogutil
import servicemanager
import subprocess
import locale
import pywintypes

import win32com.client


if win32com.client.gencache.is_readonly == True:
    win32com.client.gencache.is_readonly = False
    win32com.client.gencache.Rebuild()


import SocketServer, socket
from time import sleep
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler


TIMEOUT = 15

socket.setdefaulttimeout(TIMEOUT)



FDCONF = "C:\\Program Files\\Bacula\\bacula-fd.conf"
KEYPAR = "C:\\Program Files\\Bacula\\client.pem"
MASTERKEY = "C:\\Program Files\\Bacula\\master.cert"


# Threaded mix-in
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer):
    pass

    
    
class NimbusService(object):

    def save_keys(self, keypar, masterkey):
        with file(KEYPAR, "w") as f:
            f.write(keypar)

        with file(MASTERKEY, "w") as f:
            f.write(masterkey)

        return True
        

    def save_config(self, config):
        with codecs.open(FDCONF, "w", "utf-8") as f:
            f.write(config)
        return True



    def restart_bacula(self):
        cmd = subprocess.Popen(["sc","stop","Bacula-FD"], 
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE )
        cmd.communicate()
        sleep(3)
        cmd = subprocess.Popen(["sc","start","Bacula-FD"], 
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE )
        cmd.communicate()
        return True
        

    def get_home(self):
        return os.environ['HOME']

    def get_available_drives(self):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        return drives

    def list_dir(self, path):
        try:

                        
            def _is_dir(filename):
                if os.path.isdir(os.path.join(path, filename)):
                    return path + filename + '/'
                return path + filename


            def _convert_encoding_filename(filename):
                if not isinstance(filename, unicode):
                    return filename.decode(locale.getpreferredencoding())
                return filename
            
            files = os.listdir(path)
            files = map(_is_dir, files)
            files = [ _convert_encoding_filename(f) for f in files]
            return files
        except IOError, error:
            return []

        

class XMLRPCservice(win32serviceutil.ServiceFramework):
    _svc_name_ = "NimbusService"
    _svc_display_name_ = "NimbusService"
    _svc_description_ = "Nimbus client service"

    def __init__(self, args):
        win32evtlogutil.AddSourceToRegistry( self._svc_display_name_, 
                                             sys.executable, "Application")
        win32serviceutil.ServiceFramework.__init__(self, args)
        
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.server = AsyncXMLRPCServer( ('0.0.0.0', 11110),
                                         SimpleXMLRPCRequestHandler)

                                        
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)


    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ' (%s)' % self._svc_name_))

        self.server.register_instance(NimbusService())

        while win32event.WaitForSingleObject(self.hWaitStop, 0) ==\
                win32event.WAIT_TIMEOUT:
            self.server.handle_request()

        win32evtlogutil.ReportEvent( self._svc_name_,
                                     servicemanager.PYS_SERVICE_STOPPED,
                                     0,
                                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                                    (self._svc_name_,""))

                                    
                                    

    

    
def check_firewall_conf():
    try:
        check_firewall_app_conf("Nimbus Service for Windows Client", 
                                'C:\\Nimbus\\pkgs\\winservice.exe')
        check_firewall_app_conf("Nimbus Notifier for Windows Client", 
                                'C:\\Nimbus\\pkgs\\windowsnotifier.exe')
    except pywintypes.com_error:
        pass # firewall not initialized on boot
        
def check_firewall_app_conf(name, imagefile):

    firewall = win32com.client.gencache.EnsureDispatch('HNetCfg.FwMgr',0)
    allowed_apps = firewall.LocalPolicy.CurrentProfile.AuthorizedApplications
    
    nimbus_service_allowed = False
    
    for app in allowed_apps:
        if app.Name == name:
            nimbus_service_allowed = True
        
    if not nimbus_service_allowed:
        newapp = win32com.client.Dispatch('HNetCfg.FwAuthorizedApplication')
        newapp.Name = name
        newapp.ProcessImageFileName = imagefile
        newapp.Enabled = True
        allowed_apps.Add(newapp)


check_firewall_conf()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(XMLRPCservice)
