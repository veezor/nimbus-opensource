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



from django.shortcuts import redirect
from django.core.exceptions import MiddlewareNotUsed

from nimbus.libs import bacula
from nimbus.wizard import views
from nimbus.wizard import models

class Wizard(object):

    def __init__(self):
        wizard = models.Wizard.get_instance()
        if wizard.has_completed():
            bacula.unlock_bacula_and_start()
            raise MiddlewareNotUsed("wizard completed")

    def process_request(self, request):

        
        if not self.is_restricted_url(request):
            return None

        wizard = models.Wizard.get_instance()

        if wizard.has_completed():
            return None
        else:
            return redirect('nimbus.wizard.views.license')


    def is_restricted_url(self, request):
        path = request.META['PATH_INFO']
        if path.startswith("/wizard") or\
                path.startswith("/media") or\
                'ajax' in path:
            return False
        return True
