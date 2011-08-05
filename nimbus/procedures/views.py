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
# Create your views here.

from copy import copy
from time import strftime, strptime

from django.contrib.auth.decorators import login_required
from django.views.generic import create_update
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from pybacula import BConsoleInitError

from nimbus.bacula.models import Job
from nimbus.procedures.models import Procedure
from nimbus.computers.models import Computer
from nimbus.storages.models import Storage
from nimbus.schedules.models import Schedule
from nimbus.filesets.models import FileSet
#from nimbus.pools.models import Pool
from nimbus.shared.views import render_to_response
from nimbus.shared.forms import form, form_mapping
from nimbus.shared.enums import days as days_enum, weekdays as weekdays_enum, levels as levels_enum
from nimbus.procedures.forms import ProcedureForm, ProcedureEditForm
from nimbus.schedules.models import Schedule


@login_required
def add(request, teste=None):
    comp_id = 0
    if request.GET:
        comp_id = request.GET["comp_id"]
    title = u"Adicionar backup"
    form = ProcedureForm(prefix="procedure")
    content = {'title': title,
                'form':form,
                'comp_id': comp_id}
    if request.method == "POST":
        data = copy(request.POST)
        if data["procedure-fileset"]:
            fileset = FileSet.objects.get(id=data['procedure-fileset'])
            content['fileset'] = fileset
        if data["procedure-schedule"]:
            schedule = Schedule.objects.get(id=data['procedure-schedule'])
            content['schedule'] = schedule
        procedure_form = ProcedureForm(data, prefix="procedure")
        if procedure_form.is_valid():
            procedure = procedure_form.save()
            messages.success(request, "Procedimento de backup '%s' criado com sucesso" % procedure.name)
            return redirect('/procedures/list')
        else:
            messages.error(request, "O procedimento de backup não foi criado devido aos seguintes erros")
            content['form'] = procedure_form
            return render_to_response(request, "add_procedure.html", content)
    return render_to_response(request, "add_procedure.html", content)


@login_required
def edit(request, procedure_id):
    p = get_object_or_404(Procedure, pk=procedure_id)
    title = u"Editando '%s'" % p.name
    partial_form = ProcedureForm(prefix="procedure", instance=p)
    content = {'title': title,
              'form': partial_form,
              'id': procedure_id,
              'procedure': p,
              'schedule': p.schedule,
              'fileset': p.fileset,
              'retention_time': p.pool_retention_time}
    print content
    print content['schedule'].id
    if request.method == "POST":
        data = copy(request.POST)
        if data['procedure-schedule'] == u"":
            data['procedure-schedule'] = u"%d" % p.schedule.id
        if data['procedure-fileset'] == u"":
            data['procedure-fileset'] = u"%d" % p.fileset.id
        procedure_form = ProcedureForm(data, instance=p, prefix="procedure")
        if procedure_form.is_valid():
            procedure_form.save()
            messages.success(request, "Procedimento '%s' alterado com sucesso" % p.name)
            return redirect('/procedures/list')
        else:
            messages.error(request, "O procedimento de backup não foi criado devido aos seguintes erros")
            content['forms'] = [procedure_form]
            return render_to_response(request, "edit_procedure.html", content)
    return render_to_response(request, 'edit_procedure.html', content)


@login_required
def delete(request, object_id):
    p = get_object_or_404(Procedure, pk=object_id)
    jobs = p.all_my_jobs
    content = {'procedure': p,
               'last_jobs': jobs}
    return render_to_response(request, "remove_procedure.html", content)


@login_required
def do_delete(request, object_id):
    procedure = Procedure.objects.get(id=object_id)
    if not procedure.schedule.is_model:
        procedure.schedule.delete()
    if not procedure.fileset.is_model:
        procedure.fileset.delete()
    procedure.delete()
    messages.success(request, u"Procedimento removido com sucesso.")
    return redirect('/procedures/list')


@login_required
def execute(request, object_id):
    try:
        procedure = Procedure.objects.get(id=object_id)
        procedure.run()
        messages.success(request, u"Procedimento em execução.")
    except BConsoleInitError, error:
        messages.error(request, u"Servidor de backup inativo, impossível realizar operação.")
    return redirect('/procedures/list')

@login_required
def list_all(request):
    procedures = Procedure.objects.filter(id__gt=1)
    title = u"Procedimentos de backup"
    last_jobs = Procedure.all_jobs()[:10]
    return render_to_response(request, "procedures_list.html", locals())


@login_required
def activate(request, object_id):
    if request.method == "POST":
        procedure = Procedure.objects.get(id=object_id)
        procedure.active = True
        procedure.save()
        messages.success(request, "Procedimento ativado com sucesso")
    return redirect('/procedures/list')

@login_required
def deactivate(request, object_id):
    if request.method == "POST":
        procedure = Procedure.objects.get(id=object_id)
        procedure.active = False
        procedure.save()
        messages.success(request, "Procedimento desativado com sucesso")
    return redirect('/procedures/list')

@login_required
def profile_list(request):
    title = u"Perfis de configuração"
    filesets = FileSet.objects.filter(is_model=True)
    schedules = Schedule.objects.filter(is_model=True)
    computers = Computer.objects.filter(active=True,id__gt=1)
    content = {'title': u"Perfis de configuração",
               'filesets': filesets,
               'schedules': schedules,
               'computers': computers}
    return render_to_response(request, "profile_list.html", content)

# @login_required
# def profile_delete(request, object_id):
#     profile = get_object_or_404(Profile, pk=object_id)
#     if request.method == "POST":
#         n_procedures = Procedure.objects.filter(profile=profile).count()
#         if n_procedures:
#             messages.error(request, u"Impossível remover perfil em uso")
#         else:
#             profile.delete()
#             messages.success(request, u"Procedimento removido com sucesso.")
#             return redirect('nimbus.procedures.views.profile_list')
#     remove_name = profile.name
#     return render_to_response(request, 'remove.html', locals())
    
@login_required
def history(request, object_id=False):
    #TODO: Filtrar jobs de um procedimento específico
    title = u'Histórico de Procedimentos'
    # get page number
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    #get all jobs
    all_jobs = Procedure.all_jobs()
    paginator = Paginator(all_jobs, 20)
    try:
        jobs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        jobs = paginator.page(paginator.num_pages)
    last_jobs = jobs.object_list
    return render_to_response(request, "procedures_history.html", locals())























