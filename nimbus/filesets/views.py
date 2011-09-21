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

import traceback
import socket
import simplejson
from copy import copy
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import widgets

from nimbus.filesets.models import FileSet, FilePath
from nimbus.computers.models import Computer, NimbusClientMessageError
from nimbus.shared.views import render_to_response
from nimbus.shared.forms import form_mapping, form_from_model
from nimbus.libs.db import Session
from nimbus.shared import utils
from nimbus.filesets import forms
# import pdb

@login_required
def add(request, computer_id=None):
    computer = get_object_or_404(Computer, pk=computer_id)
    referer = utils.Referer(request)
    fileset_form = forms.FileSetForm(prefix="fileset")
    hide_name = False
    if referer.local == '/procedures/profile/list/':
        fileset_form.initial = {'is_model': True}
    elif referer.local.startswith('/procedures/'):
        fileset_form.initial = {'name': 'Conjunto de arquivos de %s' % computer.name}
        hide_name = True
    content = {'title': u"Criar conjunto de arquivos",
               'computer': computer,
               'fileset_form': fileset_form,
               'hide_name': hide_name}
    return render_to_response(request, "add_fileset.html", content)


@login_required
def do_add(request):
    if request.method == 'POST':
        data = request.POST
        fileset_form = forms.FileSetForm(data, prefix="fileset")
        if fileset_form.is_valid():
            new_fileset = fileset_form.save()
            filepaths_form = forms.FilesFormSet(data, instance=new_fileset)
            if filepaths_form.is_valid():
                filepaths_form.save()
                return HttpResponse('{"status":true,"fileset_id":"%s","fileset_name":"%s","message":"Conjunto de arquivos \'%s\' foi criado com sucesso"}' % (new_fileset.id, new_fileset.name, new_fileset.name))
            else:
                new_fileset.delete()
                return HttpResponse('{"status":false,"fileset_id":"none","message":"Erro nos arquivos","error":1}')
        else:
            return HttpResponse('{"status":false,"fileset_id":"none","message":"Erro nos fileset","error":0}')


@login_required
def edit(request, fileset_id, computer_id):
    f = FileSet.objects.get(id=fileset_id)
    fileset_form = forms.FileSetForm(prefix="fileset", instance=f)
    deletes_form = forms.FilesToDeleteForm(instance=f)
    computer = get_object_or_404(Computer, pk=computer_id)
    content = {'title': u"Editar Conjunto de Arquivos '%s'" % f.name,
               'computer': computer,
               'fileset_form': fileset_form,
               'deletes_form': deletes_form,
               'fileset': f}
    return render_to_response(request, "edit_fileset.html", content)


@login_required
def do_edit(request, fileset_id):
    f = FileSet.objects.get(id=fileset_id)
    if request.method == 'POST':
        data = request.POST
        fileset_form = forms.FileSetForm(data, prefix="fileset", instance=f)
        if fileset_form.is_valid():
            new_fileset = fileset_form.save()
            filepaths_form = forms.FilesToDeleteForm(data, instance=new_fileset)
            if filepaths_form.is_valid():
                filepaths_form.save()
                return HttpResponse('{"status":true,"fileset_id":"%s","fileset_name":"%s","message":"Conjunto de arquivos \'%s\' foi atualizado com sucesso"}' % (new_fileset.id, new_fileset.name, new_fileset.name))
            else:
                new_fileset.delete()
                return HttpResponse('{"status":false,"fileset_id":"none","message":"Erro nos arquivos","error":1}')
        else:
            return HttpResponse('{"status":false,"fileset_id":"none","message":"Erro nos fileset","error":0}')
    
@login_required
def get_tree(request):
    if request.method == "POST":
        try:
            path = request.POST['path']
            computer_id = request.POST['computer_id']
            try:
                computer = Computer.objects.get(id=computer_id)
                files = computer.get_file_tree(path)
                response = simplejson.dumps(files)
            except socket.error, error:
                response = simplejson.dumps({"type" : "error",
                                             "message" : "Impossível conectar ao cliente"})
            except Computer.DoesNotExist, error:
                response = simplejson.dumps({"type" : "error",
                                             "message" : "Computador não existe"})
            except NimbusClientMessageError, error:
                response = simplejson.dumps({"type" : "error",
                                             "message" : "Erro no cliente Nimbus."})
            return HttpResponse(response, mimetype="text/plain")
        except Exception:
            traceback.print_exc()

@login_required
def delete(request, fileset_id):
    f = get_object_or_404(FileSet, pk=fileset_id)
    procedures = f.procedures.all()
    content = {'fileset': f,
               'procedures': procedures}
    return render_to_response(request, "remove_fileset.html", content)


@login_required
def do_delete(request, fileset_id):
    f = get_object_or_404(FileSet, pk=fileset_id)
    if f.is_model:
        for procedure in f.procedures.all():
            novo_fileset = FileSet()
            novo_fileset.name = 'Arquivos de %s' % procedure.name
            novo_fileset.save()
            for file in f.files.all():
                novo_arquivo = FilePath()
                novo_arquivo.fileset = novo_fileset
                novo_arquivo.path = file.path
                novo_arquivo.save()
            procedure.fileset = novo_fileset
            procedure.save()
    name = f.name
    f.delete()
    messages.success(request, u"Perfil de conjunto de arquivos '%s' removido com sucesso." % name)
    return redirect('/procedures/profile/list')


@login_required
def reckless_discard(request):
    if request.method == 'POST':
        fileset_id = request.POST["fileset_id"]
        f = get_object_or_404(FileSet, pk=fileset_id)
        # not so reckless
        if not f.procedures.all():
            f.delete()
        # else:
            # leave it to garbage colletor
