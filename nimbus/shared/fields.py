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



import re

from django import forms
from django.db import models
from django.core.exceptions import ValidationError


path_re = re.compile('^([a-zA-Z]:)?/([a-zA-Z0-9 .@_-]+/?)*$')
NAME_RE = re.compile("^[\w\s]{4,255}$")


def check_model_name(value):
    if not NAME_RE.match(value):
        raise ValidationError("O campo deve conter apenas caracteres alfa-numéricos e espaços. O limite mínimo de caracteres é 4.")

def name_is_valid(value):
    try:
        check_model_name(value)
        return True
    except ValidationError, error:
        return False

class FormPathField(forms.CharField):
    def clean(self, value):
        super(FormPathField, self).clean(value)
        if not re.match(path_re, value):
            raise forms.ValidationError, u'Invalid format'
        return value


class ModelPathField(models.CharField):
    def formfield(self, *args, **kwargs):
        kwargs['form_class'] = FormPathField
        return super(ModelPathField, self).formfield(*args, **kwargs)



class CharFormField(forms.CharField):

    def widget_attrs(self, widget):
        attrs = super(CharFormField, self).widget_attrs(widget)

        if not attrs:
            attrs = {}

        # import pdb; pdb.set_trace()

        # if self.choices:
        #     attrs['class'] = 'styled'
        # else:
        if self.max_length < 40:
            attrs['class'] = 'text small'
        elif self.max_length < 260:
            attrs['class'] = 'text medium'
        else:
            attrs['class'] = "text big"

        return attrs

class IPAddressField(forms.IPAddressField):

    def widget_attrs(self, widget):

        attrs = super(IPAddressField, self).widget_attrs(widget)

        if not attrs:
            attrs = {}

        attrs['class'] = 'text small'

        return attrs

class ChoiceField(forms.ChoiceField):

    def widget_attrs(self, widget):
        attrs = super(ChoiceField, self).widget_attrs(widget)
        import pdb; pdb.set_trace()
        return attrs

class Select(forms.Select):

    def widget_attrs(self, widget):
        attrs = super(ComboField, self).widget_attrs(widget)
        import pdb; pdb.set_trace()
        return attrs
