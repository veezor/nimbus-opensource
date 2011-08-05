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




from os import path
from datetime import datetime

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete

from nimbus.base.models import BaseModel
from nimbus.shared import signals, utils, enums, fields
from nimbus.libs.template import render_to_file


LEVELS = tuple( (l,l) for l in enums.levels )  
WEEKDAYS = tuple( (d,d) for d in enums.weekdays )
MONTHDAYS = tuple( (d,d) for d in enums.days )


class BackupLevel(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = u"Nível de backup"

class BackupKind(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    name_pt = models.CharField(max_length=255, unique=True, null=False)

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = u"Tipo de agendamento"

class Schedule(BaseModel):
    name = models.CharField(u'Nome qualquer', max_length=255, null=False,
                            blank=False)
    is_model = models.BooleanField(default=False, null=False)



    class Meta:
        verbose_name = u"Agendamento"

    def get_runs(self):
        # runs = []
        # for obj in [self.if_month(), self.if_week(), self.if_day(), self.if_hour()]:
        #     if obj:
        #         runs += obj.bacula_config_runs()
        # return runs
        pass

    def __unicode__(self):
        return self.name

    # def if_month(self):
    #     try:
    #         return self.month
    #     except:
    #         return None
    # 
    # def if_week(self):
    #     try:
    #         return self.week
    #     except:
    #         return None
    # 
    # def if_day(self):
    #     try:
    #         return self.day
    #     except:
    #         return None
    # 
    # def if_hour(self):
    #     try:
    #         return self.hour
    #     except:
    #         return None

class Run(models.Model):
    schedule = models.ForeignKey(Schedule, related_name="runs", null=False,
                                 blank=False)
    day = models.PositiveSmallIntegerField(null=False, max_length=2)
    hour = models.CharField(null=False, max_length=2)
    minute = models.CharField(null=False, max_length=2)
    level = models.ForeignKey(BackupLevel)
    kind = models.ForeignKey(BackupKind)
    
    def __unicode__(self):
        return "%s - %s - %s - %s - %s:%s" % (self.schedule.name, self.kind.name,
                                      self.day, self.level.name, self.hour, self.minute)

    @property
    def day_string(self):
        if self.kind.name == 'weekly':
            return enums.weekdays_range[self.day]
        elif (self.kind.name == 'daily') or (self.kind.name == 'hourly'):
            return 'Todos'
        else:
            return self.day

    @property
    def bacula_config(self):
        if self.kind.name == 'monthly':
            return u"Run = Level=%s on %s at %s:%s" %(self.level, self.day, self.hour, self.minute)
        elif self.kind.name == 'weekly':
            return u"Run = Level=%s %s at %s:%s" %(self.level, enums.week_dict[int(self.day)], self.hour, self.minute)
        elif self.kind.name == 'daily':
            return u"Run = Level=%s daily at %s:%s" %(self.level, self.hour, self.minute)
        elif self.kind.name == 'hourly':
            return u"Run = Level=%s hourly at 00:%s" %(self.level, self.minute)



# class Month(models.Model):
#     active = models.BooleanField(default=True)
#     # schedule = models.ForeignKey(Schedule, related_name="months", null=False,
#     #                              blank=False)
#     # day = models.PositiveSmallIntegerField(null=False, max_length=2)
#     days = models.CommaSeparatedIntegerField(null=False, max_length=255)
#     schedule = models.OneToOneField(Schedule)
#     hour = models.TimeField()
#     level = models.ForeignKey(BackupLevel)
# 
#     def __unicode__(self):
#         return self.schedule.name
# 
#     def bacula_config_runs(self):
#         block = []
#         day_list = self.days.split(',')
#         for day in day_list:
#             line = "Run = Level=%s on %s at %s" %(self.level, day, 
#                                                   self.hour.strftime('%H:%M'))
#             block.append(line)
#         return block
# 
#     def human_readable(self):
#         lines = []
#         day_list = self.days.split(',')
#         for day in day_list:
#             line = u"Mensal: Dia %s às %s. Backup %s" %(day, 
#                                                     self.hour.strftime('%H:%M'),
#                                                     self.level)
#             lines.append(line)
#         return lines
# 
# class Week(models.Model):
#     active = models.BooleanField(default=True)
#     # schedule = models.ForeignKey(Schedule, related_name="weeks", null=False,
#     #                              blank=False)
#     # day = models.PositiveSmallIntegerField(null=False, max_length=1)
#     schedule = models.OneToOneField(Schedule)
#     days = models.CommaSeparatedIntegerField(null=False, max_length=255)
#     hour = models.TimeField()
#     level = models.ForeignKey(BackupLevel)
# 
#     def __unicode__(self):
#         return self.schedule.name
# 
#     def bacula_config_runs(self):
#         weekdays = enums.week_dict
#         block = []
#         day_list = self.days.split(',')
#         for day in day_list:
#             line = u"Run = Level=%s %s at %s" %(self.level, weekdays[int(day)],
#                                                self.hour.strftime('%H:%M'))
#             block.append(line)
#         return block
# 
#     def human_readable(self):
#         weekdays = enums.weekdays_range
#         lines = []
#         day_list = self.days.split(',')
#         for day in day_list:
#             line = u"Semanal: %s às %s. Backup %s" %(weekdays[int(day)], 
#                                                     self.hour.strftime('%H:%M'),
#                                                     self.level)
#             lines.append(line)
#         return lines
# 
# class Day(models.Model):
#     active = models.BooleanField(default=True)
#     schedule = models.OneToOneField(Schedule)
#     # schedule = models.ForeignKey(Schedule, related_name="days", null=False,
#     #                              blank=False)
#     hour = models.TimeField()
#     level = models.ForeignKey(BackupLevel)
# 
#     def __unicode__(self):
#         return self.schedule.name
#         
#     def bacula_config_runs(self):
#         line = u"Run = Level=%s daily at %s" %(self.level,
#                                               self.hour.strftime('%H:%M'))
#         return [line]
# 
#     def human_readable(self):
#         return u"Diário às %s. Backup %s" %(self.hour.strftime('%H:%M'),
#                                             self.level)
# 
# class Hour(models.Model):
#     active = models.BooleanField(default=True)
#     schedule = models.OneToOneField(Schedule)
#     # schedule = models.ForeignKey(Schedule, related_name="hours", null=False,
#     #                              blank=False)
#     minute = models.PositiveSmallIntegerField()
#     level = models.ForeignKey(BackupLevel)
# 
#     def __unicode__(self):
#         return self.schedule.name
# 
#     def bacula_config_runs(self):
#         line = u"Run = Level=%s hourly at 00:%02d" %(self.level, self.minute)
#         return [line]
# 
#     def human_readable(self):
#         return u"De hora em hora aos %02d minutos. Backup %s" %(self.minute,
#                                                                 self.level)


def update_schedule_file(schedule):
    name = schedule.bacula_name
    filename = path.join(settings.NIMBUS_SCHEDULES_DIR, name)
    render_to_file(filename,
                   "schedule",
                   name=name,
                   runs=schedule.runs.all())


def remove_schedule_file(schedule):
    name = schedule.bacula_name
    filename = path.join(settings.NIMBUS_SCHEDULES_DIR, name)
    utils.remove_or_leave(filename)


def update_schedule(run):
    update_schedule_file(run.schedule)
    

signals.connect_on(update_schedule_file, Schedule, post_save)
signals.connect_on(update_schedule, Run, post_save)
signals.connect_on(remove_schedule_file, Schedule, post_delete)
signals.connect_on(update_schedule, Run, post_delete)
