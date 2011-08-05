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



import copy

from django import forms
from django.forms import widgets

from django.db import models

from nimbus.shared.fields import CharFormField, IPAddressField

SELECT_ATTRS = {"class": ""}
INPUT_ATTRS = {"class":"text"}

class InvalidMapping(Exception):
    pass



def make_custom_fields(f, *args, **kwargs):
    # import pdb; pdb.set_trace()
    
    if f.choices or isinstance(f, models.ForeignKey):
        kwargs.pop('widget', None)
        return f.formfield(widget=forms.Select(attrs=SELECT_ATTRS), **kwargs)
    if isinstance(f, models.IPAddressField):
        return f.formfield(form_class=IPAddressField, **kwargs)
    elif isinstance(f, models.CharField):
        return f.formfield(widget=widgets.TextInput(attrs=INPUT_ATTRS), **kwargs)
    elif isinstance(f, models.TimeField):
        return f.formfield(widget=widgets.TextInput(attrs=INPUT_ATTRS), **kwargs)
    elif isinstance(f, models.PositiveSmallIntegerField):
        return f.formfield(widget=widgets.TextInput(attrs=INPUT_ATTRS), **kwargs)
    elif isinstance(f, models.ManyToManyField):
        kwargs.pop('widget', None)
        return f.formfield(widget=forms.SelectMultiple(attrs=SELECT_ATTRS), **kwargs)
    else:
        return f.formfield(**kwargs)


def form(modelcls):

    class Form(forms.ModelForm):

        formfield_callback = make_custom_fields

        class Meta:
            model = modelcls

    return Form



def form_from_model(model):
    formclass = form(model.__class__)
    f = formclass({}, instance=model)
    f.data.update( f.initial )
    return f

def form_mapping(modelcls, query_dict, fieldname_list=None, object_id=None):


    mapping_table = {}

    if not fieldname_list:
        clsname = modelcls.__name__.lower()
        fieldname_list = [ name for name in query_dict.keys() if name.startswith(clsname) ]

    meta = modelcls._meta
    modelfields = meta.get_all_field_names()
    modelfields.remove('id')


    fieldlist = copy.copy(modelfields)

    for field in fieldlist:
        try:
            fieldobj = meta.get_field(field)

            if not fieldobj.editable:
                modelfields.remove(field)

        except models.FieldDoesNotExist, error:
            modelfields.remove(field)


    modelfields = [ field for field in modelfields \
                        if not isinstance( meta.get_field(field), models.ManyToManyField) ]


    for field in fieldlist:
        for user_field_name in fieldname_list:
            if field in user_field_name:
                mapping_table[user_field_name] = field
                break


    if len(modelfields) != len(fieldname_list):
        raise InvalidMapping("Not match: %s != %s" % (modelfields, fieldname_list))


    data = {}

    for user_field_name,form_field_name in mapping_table.items():
        data[form_field_name] = query_dict[user_field_name]

    FormClass = form(modelcls)

    if object_id:
        instance = modelcls.objects.get(id=object_id)
        return FormClass(data, instance=instance)

    return FormClass(data)


