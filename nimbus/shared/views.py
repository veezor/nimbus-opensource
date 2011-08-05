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


from django.http import Http404
from django.views.generic.create_update import update_object, create_object
from django.shortcuts import render_to_response as _render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages

from nimbus.shared.utils import block_ie_browser


from nimbus.shared import forms

def edit_singleton_model(request, templatename, redirect_to, 
                         formclass = None, model = None, extra_context = None):

    if not formclass and model:
        formclass = forms.form(model)
    try:
        return update_object( request, object_id=1, 
                              form_class = formclass, 
                              model = model,
                              template_name = templatename, 
                              post_save_redirect = reverse(redirect_to),
                              extra_context = extra_context )
    except Http404, error:
        return create_object( request, 
                              form_class = formclass, 
                              model = model,
                              template_name = templatename, 
                              post_save_redirect = reverse(redirect_to),
                              extra_context = extra_context )

def render_to_response(request, template, dictionary):
    # renderiza a mensagem de erro para o internet explorer
    # esta chamada esta aqui por se tratar de um evento global, evitando repeticao
    block_ie_browser(request)
    return _render_to_response( template, dictionary,
                                context_instance=RequestContext(request))
            


