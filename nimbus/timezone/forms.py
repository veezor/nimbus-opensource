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



from pytz import country_timezones

from django import forms
from django.forms import ModelForm, ValidationError
from nimbus.timezone.models import Timezone, COUNTRY_CHOICES
from nimbus.shared.forms import make_custom_fields


class TimezoneForm(ModelForm):
    area = forms.ChoiceField(label='Região', choices=[('', '----------')],
            widget=forms.Select(attrs={'class': 'uniform'}))
    country = forms.ChoiceField(label='País', choices=COUNTRY_CHOICES,
            widget=forms.Select(attrs={'class': 'uniform'}))

    formfield_callback = make_custom_fields

    def __init__(self, data=None, *args, **kwargs):
        super(TimezoneForm, self).__init__(data, *args, **kwargs)

        instance = kwargs.get("instance")
        if instance:
            self.load_area(instance.country)
        if data:
            self.load_area( data.get("country") )

    class Meta:
        model = Timezone
        exclude = ("uuid",)
    
    def load_area(self, country=None):
        if country:
            self.fields['area'].choices = \
                [ (a,a) for a in sorted(country_timezones[country])]
        else:
            self.fields['area'].choices = [('', '----------')]


    def clean_area(self):
        area = self.data.get("area")
        country = self.data.get("country")
        if area in country_timezones[country]:
            return area
        else:
            raise ValidationError("error")


