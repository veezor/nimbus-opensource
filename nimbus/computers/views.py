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
import socket
import xmlrpclib
import logging
import uuid

from django.contrib.auth.decorators import login_required
from django.views.generic import create_update
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError

from nimbus.computers.models import Computer, ComputerGroup, ComputerAlreadyActive
from nimbus.procedures.models import Procedure
from nimbus.bacula.models import Job
from nimbus.shared.views import render_to_response
from nimbus.shared import enums
from nimbus.shared.forms import form
from nimbus.computers import forms as forms

@login_required
def add(request):
    lforms = [ forms.ComputerForm ]
    content = {'title':u'Adicionar Computador',
               'forms':lforms,
               'computers':Computer.objects.filter(active=False)
              }
    return render_to_response(request, "computers_add.html", content)

@login_required
def edit_no_active(request, object_id):
    extra_context = {'title': u"Editar computador"}
    messages.warning(request, u"O computador ainda não foi ativado.")
    return create_update.update_object(request,
                                       object_id = object_id,
                                       model = Computer,
                                       #form_class = form(Computer),
                                       form_class = forms.ComputerForm,
                                       template_name = "base_computers.html",
                                       extra_context = extra_context,
                                       post_save_redirect = reverse("nimbus.computers.views.add"))

@login_required
def new(request):
    if request.method == "POST":
        logger = logging.getLogger(__name__)
        try:
            os = request.POST['os']
            if os not in enums.operating_systems:
                return HttpResponse(status=400)
            name = request.META.get('REMOTE_HOST')
            if not name:
                name = u"Adicionado automaticamente %s" % uuid.uuid4().hex
            address = request.META['REMOTE_ADDR']
            if Computer.objects.filter(address=address).count():
                logger.error("Já existe computador com esse ip")
                return HttpResponse(status=400)
            computer = Computer(name = name,
                                address = address,
                                operation_system=os,
                                description="Computador identificado automaticamente")
            computer.save()
            logger.info("Computador adicionado com sucesso")
            return HttpResponse(status=200)
        except (KeyError, IntegrityError), e:
            logger.exception("Erro ao adicionar o computador")
            return HttpResponse(status=400)

@login_required
def edit(request, object_id):
    extra_context = {'title': u"Editar computador"}
    return create_update.update_object(request, 
                                       object_id = object_id,
                                       model = Computer,
                                       form_class = form(Computer),
                                       template_name = "base_computers.html",
                                       extra_context = extra_context,
                                       post_save_redirect = "/computers/")


@login_required
def delete(request, object_id):
    c = get_object_or_404(Computer, pk=object_id)
    jobs = c.all_my_jobs
    content = {'computer': c,
               'last_jobs': jobs,
               'procedures': c.procedure_set.all()}
    return render_to_response(request, "remove_computer.html", content)

@login_required
def do_delete(request, object_id):
    computer = Computer.objects.get(id=object_id)
    computer.delete()
    messages.success(request, u"Computador removido com sucesso.")
    return redirect('nimbus.computers.views.list')

@login_required
def list(request):
    group = request.GET.get("group")
    if group:
        computers = Computer.objects.filter(active=True,id__gt=1, groups__name=group)
    else:
        computers = Computer.objects.filter(active=True,id__gt=1)


    groups = ComputerGroup.objects.order_by('name')
    extra_content = {
            'computers': computers,
            'title': u"Computadores Ativos",
            'groups': groups
    }
    return render_to_response(request, "computers_list.html", extra_content)

@login_required
def view(request, object_id):
    computer = Computer.objects.get(id=object_id)
    running_jobs = computer.running_jobs()
    running_procedures_content = []
    try:
        for job in running_jobs:
            running_procedures_content.append({
                    'type' : 'ok',
                    'label' : job.procedure.name,
                    'date' : job.starttime,
                    'tooltip' : job.status_message,
                    'message' : u'Computador : %s' % job.client.computer.name
                    })
    except (Procedure.DoesNotExist, Computer.DoesNotExist), error:
        pass

    last_jobs = computer.last_jobs()
    last_procedures_content = []
    try:
        for job in last_jobs:
            last_procedures_content.append({
                    'type' : job.status_friendly,
                    'label' : job.procedure.name,
                    'date' : job.endtime,
                    'tooltip' : job.status_message,
                    'message' : u'Computador : %s' % job.client.computer.name
                    })
    except (Procedure.DoesNotExist, Computer.DoesNotExist), error:
        pass


    errors_jobs = computer.error_jobs()
    errors_procedures_content = []
    try:
        for job in errors_jobs:
            errors_procedures_content.append({
                    'type' : job.status_friendly,
                    'label' : job.procedure.name,
                    'date' : job.endtime,
                    'tooltip' : job.status_message,
                    'message' : u'Computador : %s' % job.client.computer.name
                    })
    except (Procedure.DoesNotExist, Computer.DoesNotExist), error:
        pass
    backups_em_execucao = [{'title': u'Backups em Execução',
                            'content': running_procedures_content}]
    backups_com_falhas = [{'title': u'Últimos backups executados',
                           'content': last_procedures_content  },
                          {'title': u'Backups com falha',
                           'content': errors_procedures_content}]
    extra_content = {'computer': computer,
                     'title': u"Visualizar computador",
                     'backups_em_execucao': backups_em_execucao,
                     'backups_executados_e_com_falhas': backups_com_falhas,
                     }
    return render_to_response(request, "computers_view.html", extra_content)

@login_required
def group_add(request):
    if 'name' in request.POST:
        name = request.POST['name']
    else:
        name = u'Criação'
    try:
        group = ComputerGroup(name=name)
        group.save()
    except Exception, e:
        response = dict(message='error')
    else:
        response = dict(message='success')
    return HttpResponse(simplejson.dumps(response))

@login_required
def group_list(request):
    ajax = request.POST['ajax']
    if not ajax:
        return redirect('/')
    groups = ComputerGroup.objects.all()
    response = serializers.serialize("json", groups)
    return HttpResponse(response, mimetype="text/plain")

@login_required
def activate(request, object_id):
    try:
        computer = Computer.objects.get(id=object_id)
        computer.activate()
    except Computer.DoesNotExist, error:
        messages.error(request, u'Impossível ativar computador, computador inexistente')
        return redirect('nimbus.computers.views.add')
    except ComputerAlreadyActive, error:
        messages.info(request, "O computador já esta ativo")
        return redirect('nimbus.computers.views.list')
    except (socket.error, xmlrpclib.Fault), error:
        messages.error(request, u'Impossível ativar computador, verifique a conexão')
        return redirect('nimbus.computers.views.list')
    messages.success(request, u'Computador ativado com sucesso.')
    return redirect('nimbus.computers.views.list')

@login_required
def deactivate(request, object_id):
    try:
        computer = Computer.objects.get(id=object_id)
        computer.deactivate()
    except Computer.DoesNotExist, error:
        messages.error(request, u'Impossível desativar computador, computador inexistente')
        return redirect('nimbus.computers.views.list')
    messages.success(u'Computador desativado com sucesso.')
    return redirect('nimbus.computers.views.list')

def configure(request, object_id):
    try:
        computer = Computer.objects.get(id=object_id)
        computer.configure()
        messages.success(request, u'Computador reconfigurado com sucesso.')
    except IOError as (errno, strerror):
        messages.error(request, u'Erro interno. {0}: {1}'.format(errno, strerror))
    return redirect('nimbus.computers.views.list')
