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
# -*- coding: utf-8 -*-

from functools import wraps

from django.core.urlresolvers import reverse
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import Http404

from nimbus.config.models import Config
from nimbus.network.models import (NetworkInterface, 
                                   get_raw_network_interface_address)
from nimbus.timezone.forms import TimezoneForm
from nimbus.shared.views import edit_singleton_model, render_to_response
from nimbus.shared.forms import form
from nimbus.shared.utils import project_port
from nimbus.wizard import models


def only_wizard(view):
    @wraps(view)
    def wrapper(request):
        wizard = models.Wizard.get_instance()
        if wizard.has_completed():
            raise Http404()
        else:
            return view(request)

    return wrapper

@only_wizard
def license(request):
    extra_context = {
        'wizard_title': u'1 de 4 - Licença',
        'page_name': u'license',
        'wide': 'wide'
    }
    if request.method == "GET":
        return render_to_response( request, "license.html", extra_context )
    elif request.method == "POST":
        return redirect('nimbus.wizard.views.network')
    else:
        raise Http404()



@only_wizard
def network(request):
    extra_context = {'wizard_title': u'2 de 4 - Configuração de Rede',
                     'page_name': u'network'}
    if request.method == "GET":
        interface = NetworkInterface.get_instance()
        Form = form(NetworkInterface)
        extra_context['form'] = Form(instance=interface)
        return render_to_response( request, "generic.html", extra_context)
    else:
        edit_singleton_model(request, "generic.html",
                             "nimbus.wizard.views.timezone",
                              model = NetworkInterface,
                              extra_context = extra_context)

        interface = NetworkInterface.get_instance()


        if interface.address == get_raw_network_interface_address():
            return redirect( "nimbus.wizard.views.timezone" )
        else:
            return render_to_response(request, "redirect.html", 
                                        dict(ip_address=interface.address,
                                             url=reverse('nimbus.wizard.views.timezone')))



@only_wizard
def timezone(request):
    extra_context = {
        'wizard_title': u'3 de 4 - Configuração de Hora',
        'page_name': u'timezone',
        'previous': reverse('nimbus.wizard.views.network')
    }
    return edit_singleton_model( request, "generic.html",
                                 "nimbus.wizard.views.password",
                                 formclass = TimezoneForm,
                                 extra_context = extra_context )



@only_wizard
def password(request):
    extra_context = {
        'wizard_title': u'4 de 4 - Senha do usuário admin',
        'page_name': u'password',
        'previous': reverse('nimbus.wizard.views.timezone')
    }
    user = User.objects.get(id=1)
    if request.method == "GET":
        extra_context['form'] = SetPasswordForm(user)
        return render_to_response( request, "generic.html", extra_context )
    elif request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('nimbus.wizard.views.finish')
        else:
            extra_context['form'] = SetPasswordForm(user)
            extra_context['messages'] = [u'Please fill all fields.']
            return render_to_response( request, "generic.html", extra_context )
    else:
        raise Http404()


@only_wizard
def finish(request):

    #GET OR POST
    wizard = models.Wizard.get_instance()
    wizard.finish()

    network_interface = NetworkInterface.get_instance()
    if network_interface.address == get_raw_network_interface_address():
        return redirect( "nimbus.base.views.home" )
    else:
        network_interface.save() # change ip address
        return render_to_response(request, "redirect.html", dict(ip_address=network_interface.address,
                                                                 url="/"))

