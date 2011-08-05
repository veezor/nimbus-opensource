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


# -*- coding: UTF-8 -*-

from nimbus.computers import models
from django import forms
from django.forms import widgets
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from nimbus.shared import forms as nimbus_forms
from django.forms import models as django_models

class TriggerBaseForm(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(TriggerBaseForm, self).add_fields(form, index)
        form.fields['active'] = forms.BooleanField()

def make_form(modeltype, exclude_fields=None):

    class Form(forms.ModelForm):
        formfield_callback = nimbus_forms.make_custom_fields
        class Meta:
            model = modeltype
            exclude = exclude_fields

    return Form

class ComputerForm(django_models.ModelForm):
    name = forms.CharField(label=u'Nome do Computador', widget=widgets.TextInput(attrs={'class': 'text'}))
    address = forms.CharField(label=u'Endereço de Rede', widget=widgets.TextInput(attrs={'class': 'text'}))
    
    class Meta:
        model = models.Computer

class ComputerGroupForm(django_models.ModelForm):
    class Meta:
        model = models.ComputerGroup

#ComputerForm = make_form(models.Computer)