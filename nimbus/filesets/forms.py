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

from nimbus.filesets.models import *
from django import forms
from django.forms import widgets
from nimbus.shared import forms as nimbus_forms


class FileSetForm(forms.ModelForm):
    name = forms.CharField(label=u"Nome", widget=widgets.TextInput(attrs={'class': 'text small'}))
    # is_model = forms.BooleanField(widget=widgets.HiddenInput(attrs={'value': '0'}))
    class Meta:
        model = FileSet


class FilePathForm(forms.ModelForm):
    path = forms.CharField(label=u"Arquivo", widget=widgets.TextInput(attrs={'class': 'text small'}))
    class Meta:
        model = FilePath
    
FilesFormSet = forms.models.inlineformset_factory(FileSet, FilePath, can_delete=False, extra=0)

class FilesToDeleteForm(FilesFormSet):
    
    def __init__(self, data=None, *args, **kwargs):
        super(FilesToDeleteForm, self).__init__(data, *args, **kwargs)
        for f in self.forms:
            f.fields['DELETE'].widget.attrs = {'class': 'no-style'}
            f.fields['path'].widget.attrs = {'readonly': 'readonly'}
            # f.fields['path'].widget = forms.HiddenInput()
            
    can_delete = True
    form = FilePathForm