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



import systeminfo

from django.http import Http404, HttpResponse
from django.views.generic import create_update
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from nimbus.storages.models import Storage
from nimbus.procedures.models import Procedure
from nimbus.computers.models import Computer
from nimbus.shared.views import render_to_response
from nimbus.shared.forms import form
from nimbus.bacula.models import Job

@login_required
def new(request):

    if request.method == "POST":
        try:
            password = request.POST['password']

            name = request.META.get('REMOTE_HOST')
            if not name:
                name = u"Adicionado automaticamente"

            storage =  Storage(name = name,
                                address = request.META['REMOTE_ADDR'],
                                password= request.POST['password'],
                                description="Armazenamento identificado automaticamente")
            storage.save()

            return HttpResponse(status=200)
        except (KeyError, IntegrityError), e:
            return HttpResponse(status=400)



@login_required
def add(request):
    title = u"Adicionar armazenamento"
    storages = Storage.objects.filter(active=False)
    return render_to_response(request, "storages_add.html", locals())



@login_required
def edit(request, object_id):
    extra_context = {'title': u"Editar armazenamento"}
    return create_update.update_object( request,
                                        object_id = object_id,
                                        model = Storage,
                                        form_class = form(Storage),
                                        template_name = "storages_edit.html",
                                        extra_context = extra_context,
                                        post_save_redirect = "/storages/list")


@login_required
def list(request):
    d = {
        "storages" : Storage.objects.filter(active=True),
        "title": u"Armazenamento"
    }

    return render_to_response(request, "storages_list.html", d)

    # extra_content = {"object_list": Device.objects.all()}
    # return render_to_response(request, "list_storages.html", extra_content)


@login_required
def view(request, object_id):
    storage = Storage.objects.get(id=object_id)

    running_status = ('R','p','j','c','d','s','M','m','s','F','B')
    running_jobs = Job.objects.filter( jobstatus__in=running_status)\
                                 .order_by('-starttime').distinct()[:5]


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


    backups_em_execucao = [{
        'title': u'Backups em Execução',
        'content': running_procedures_content
    }]

    diskinfo = systeminfo.DiskInfo("/bacula")
    try:
        diskusage = diskinfo.get_usage()
    except OSError, error:
        messages.error(request, "Partição /bacula não encontrada")
        diskusage = 0


    d = {
        "storage" : storage,
        "title": u"Armazenamento",
        "backups_em_execucao": backups_em_execucao,
        "espaco_em_disco": diskusage
    }

    return render_to_response(request, "storages_view.html", d)


@login_required
def view_computer(request, object_id):
    storage = Storage.objects.get(id=object_id)
    computers = Computer.objects.filter(procedure__profile__storage=storage)
    d = {
        "storage" : storage,
        "computers" : computers,
        "title": u'Computadores do armazenamento "%s"' % storage.name
    }
    return render_to_response(request, "computers_list.html", d)


@login_required
def activate(request, object_id):
    storage = Storage.objects.get(id=object_id)
    storage.active = True
    storage.save()

    messages.success(request, u'Armazenamento ativado com sucesso.')
    return redirect('/storages/list')


@login_required
def deactivate(request, object_id):
    storage = Storage.objects.get(id=object_id)
    storage.active = False
    storage.save()

    return redirect('/storages/list')
