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

import re

from django.db.models import Q
from nimbus.procedures.models import *
from django import forms
from django.utils.translation import ugettext as _


class ProcedureForm(forms.ModelForm):

    def __init__(self, data=None, *args, **kwargs):
        super(ProcedureForm, self).__init__(data, *args, **kwargs)
        p = Procedure.objects.filter(name__startswith="Backup #").order_by("id")
        if p:
            index_string = p[len(p) - 1].name.split("#")[1]
            match = re.search("(\d+)", index_string)
            if match:
                next_id = int(match.group()) + 1
            else:
                next_id = 1
        else:
            next_id = 1
        name_sugestion = "Backup #%02d" % next_id
        self.fields['name'] = forms.CharField(initial=name_sugestion)
        # Se houver apenas uma opcao num ChoiceField a opção NULL sera removida
        for field in self.fields:
            if isinstance(self.fields[field], forms.models.ModelChoiceField):
                not_model_filter(field, self.fields[field])
                if field not in ['schedule', 'fileset']:
                    remove_null_choice(self.fields[field])
                else:
                    self.fields[field].empty_label = u"-ou escolha um perfil-"


    computer = forms.models.ModelChoiceField(label=_("Computador"),
                                             queryset=Computer.objects.filter(id__gt=1))
    # name = forms.CharField(initial=self.name_sugestion)

    pool_retention_time = forms.IntegerField(label="Tempo de retenção",
                                             min_value=1, max_value=9999,
                                             initial=10)
                                             # widget=forms.HiddenInput())
    fileset = forms.models.ModelChoiceField(label=_("Conjunto de arquivos"),
                                            queryset=FileSet.objects.filter(id__gt=1),
                                            empty_label = u"-ou escolha um perfil-")
    schedule = forms.models.ModelChoiceField(label=_("Agendamento"),
                                             queryset=Schedule.objects.filter(id__gt=1),
                                             empty_label = u"-ou escolha um perfil-")

    class Meta:
        model = Procedure
        fields = ('computer',
                  'schedule',
                  'fileset',
                  'storage',
                  'pool_retention_time',
                  'name')
        exclude = ('active', 'pool_size', 'pool_name')


class ProcedureEditForm(forms.ModelForm):

    def __init__(self, data=None, *args, **kwargs):
        super(ProcedureEditForm, self).__init__(data, *args, **kwargs)
        instance = kwargs.get("instance")
        f_id = instance.fileset.id
        self.fields['fileset'] = forms.models.ModelChoiceField(
                                            label=_("Fileset"), required=False,
                                            queryset=FileSet.objects.filter(
                                                Q(is_model=True) | Q(id=f_id)))
        s_id = instance.schedule.id
        self.fields['schedule'] = forms.models.ModelChoiceField(
                                            label=_("Schedule"), required=False,
                                            queryset=Schedule.objects.filter(
                                                Q(is_model=True) | Q(id=s_id)))
                                                
    pool_retention_time = forms.IntegerField(label="Tempo de retenção",
                                             min_value=1, max_value=9999)
                                             # widget=forms.HiddenInput())
                                
    class Meta:
        model = Procedure
        fields = ('active',
                  'name',
                  'computer',
                  'schedule',
                  'fileset',
                  'storage',
                  'pool_retention_time')
        exclude = ('pool_size', 'pool_name')


def remove_null_choice(field_object):
    current_choices = field_object.choices
    if len(current_choices) == 1:
        choices = []
        for choice in current_choices:
            if choice[0] != u'':
                choices.append(choice)
        field_object.choices = choices


def not_model_filter(field_name, field_object):
    # choice_forms = [{'field': 'schedule', 'object': Schedule},
    #          {'field': 'fileset', 'object': FileSet}]
    # for cform in choice_forms:
    choice_forms = {'schedule': Schedule, 'fileset': FileSet}
    if choice_forms.has_key(field_name):    
        choices = []
        current_choices = field_object.choices
        for choice in current_choices:
            if choice[0] != u'':
                if choice_forms[field_name].objects.get(id=choice[0]).is_model:
                    choices.append(choice)
            else:
                choices.append(choice)
        field_object.choices = choices
