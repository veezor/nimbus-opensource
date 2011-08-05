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


# -*- coding: utf-8 -*-



import simplejson
from os.path import getsize

from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.core import validators


from nimbus.shared.views import render_to_response
from nimbus.shared import utils, middlewares
import networkutils 
import systeminfo




@login_required
def network_tool(request, type="ping"):
    if type == "ping":
        title = u"Teste de ping"
    elif type == "traceroute":
        title = u"Teste de traceroute"
    elif type == "nslookup":
        title = u"Teste de ns lookup"
    
    extra_content = {'title': title, 'type': type}
    
    return render_to_response(request, "system_network_tool.html", extra_content)


@login_required
def create_or_view_network_tool(request):


    if request.method  == "POST":
    
        rtype = request.POST['type']
        ip = request.POST['ip']
        is_url = False

        try:
            try:
                validators.validate_ipv4_address(ip) # ip format x.x.x.x
            except ValidationError, error: # url format www.xxx.xxx
                value = ip
                if not '://' in value:
                    value = 'https://%s' % value
                urlvalidator = validators.URLValidator()
                urlvalidator(value)
                is_url  = True

            if rtype == "ping":
                rcode, output = networkutils.ping(ip)
            elif rtype == "traceroute":
                rcode, output = networkutils.traceroute(ip)
            elif rtype == "nslookup":
                try:
                    if is_url:
                        output = networkutils.resolve_name(ip)
                    else:
                        output = networkutils.resolve_addr(ip)
                except (networkutils.HostAddrNotFound,
                         networkutils.HostNameNotFound), error:
                    output = "Não encontrado"

        except ValidationError, error:
            output = "\n".join(error.messages)
        

        response = simplejson.dumps({'msg': output})
        return HttpResponse(response, mimetype="text/plain")

