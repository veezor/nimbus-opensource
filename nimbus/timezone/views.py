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



# Create your views here.


import json
from pytz import country_timezones

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from nimbus.timezone.forms import TimezoneForm
from nimbus.shared.views import edit_singleton_model, render_to_response
from nimbus.shared.forms import form, form_mapping
from django.contrib import messages


@login_required
def timezone_conf(request):
    return edit_singleton_model( request, "timezoneconf.html", 
                                 "nimbus.timezone.views.timezone_conf",
                                 formclass = TimezoneForm )


def area_request(request):
    if request.is_ajax() and request.method == 'POST':
        country = request.POST.get('country', {})
        areas = sorted(country_timezones.get(country, []))
        response = json.dumps(areas)

        return HttpResponse(response, mimetype="application/json")
