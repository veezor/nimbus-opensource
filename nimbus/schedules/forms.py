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


# # -*- coding: utf-8 -*-
# 
# from django import forms
# from django.core.exceptions import ObjectDoesNotExist
# from django.forms.models import inlineformset_factory, BaseInlineFormSet
# 
# from nimbus.schedules import models
# from nimbus.shared import forms as nimbus_forms
# 
# 
# class ScheduleForm(forms.ModelForm):
#     name = forms.CharField(label="Nome do agendamento", widget=forms.TextInput(
#                                                 attrs={'class':'text small'}))
#     class Meta:
#         model = models.Schedule
# 
# 
# class MonthForm(forms.ModelForm):
#     active = forms.BooleanField(widget=forms.CheckboxInput(
#                         attrs={'class':'schedule_activate', 'id': 'month'}))
#     hour = forms.CharField(label="Hora", widget=forms.TextInput(
#                                     attrs={'class':'text small mascara_hora'}))
#     days = forms.CharField(widget=forms.HiddenInput())
#     
#     class Meta:
#         model = models.Month
# 
# 
# class HourForm(forms.ModelForm):
#     active = forms.BooleanField(widget=forms.CheckboxInput(
#                             attrs={'class':'schedule_activate', 'id': 'hour'}))
#     minute = forms.IntegerField(label="Minuto da hora",
#                                 min_value=0, max_value=59,
#                                 initial=00,
#                                 widget=forms.TextInput(
#                                                 attrs={'class':'text small'}))# mascara_minuto'}))
#     class Meta:
#         model = models.Hour
# 
# 
# class WeekForm(forms.ModelForm):
#     active = forms.BooleanField(widget=forms.CheckboxInput(
#                             attrs={'class':'schedule_activate', 'id': 'week'}))
#     hour = forms.CharField(label=u'Hora', widget=forms.TextInput(
#                                     attrs={'class':'text small mascara_hora'}))
#     days = forms.CharField(widget=forms.HiddenInput())
# 
#     class Meta:
#         model = models.Week
# 
# 
# class DayForm(forms.ModelForm):
#     active = forms.BooleanField(widget=forms.CheckboxInput(
#                             attrs={'class':'schedule_activate', 'id': 'day'}))
#     hour = forms.CharField(label=u'Hora', widget=forms.TextInput(
#                                     attrs={'class':'text small mascara_hora'}))
#     class Meta:
#         model = models.Day
# 
