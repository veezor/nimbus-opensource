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



import datetime
import cPickle as pickle
from threading import Lock
from contextlib import nested
from urllib2 import URLError

from django.conf import settings

import systeminfo

def _sort_key_function(date):
    day, month, year = date
    return (year, month, day)


class GraphDataManager(object):
    """ data = {'data' :
                    {
                  '<date>' : {
                    'disk' : number
                   }
              },
            'last_update' : <datetime>
         } """
    MAX_DAYS = 7

    def __init__(self):
        self.filename = settings.NIMBUS_GRAPHDATA_FILENAME
        self.lock = Lock()
        self.data = None
        self.open()
        #self.update()

    def open(self):
        try:
            with nested(file(self.filename),self.lock) as (fileobj, lock):
                self.data = pickle.load(fileobj)
        except IOError, error:
            now = datetime.datetime.now()
            last_update = now - datetime.timedelta(seconds=600)
            self.data = {"data" : {},
                         "last_update" : last_update}

    def save(self, data):
        with nested(file(self.filename, "w"),self.lock) as (fileobj, lock):
            pickle.dump(data, fileobj)


    def get_disk_data(self):
        try:
            diskinfo = systeminfo.DiskInfo("/bacula")
            diskusage = diskinfo.get_used()
            return diskusage
        except OSError, error:
            return 0.0

    def _list_measures(self, datatype):
        data = self.data['data']
        measures = []
        try:
            for date in sorted(data, key=_sort_key_function):
                fmt_date = "/".join([str(x) for x in date])
                value = data[date][datatype]
                measures.append((fmt_date, value))
        except KeyError:
            pass
        
        self._complete_measures(measures)
        return measures


    def _complete_measures(self, measures):
        if len(measures) > 1:
            day = measures[0][0] # first (date, value)
            day = datetime.datetime.strptime(day + " 00:00", "%d/%m/%Y %H:%M")
        else:
            day = datetime.datetime.now()

        needs =  self.MAX_DAYS - len(measures)
        for d in xrange(1, needs + 1):
            diff = datetime.timedelta(days=d)
            old_day = day - diff
            old_day_str = "%d/%d/%d" % (old_day.day, old_day.month, old_day.year)
            measures.insert(0, (old_day_str, 0))


#    def _list_days(self):
#        now = datetime.datetime.now()
#        days = []
#
#        for i in xrange(self.MAX_DAYS - 1,0,-1):
#            diff = datetime.timedelta(days=i)
#            days.append( now - diff )
#
#        days.append(now)
#
#        return [ d.strftime("%d/%m/%y") for d in days ]

    def list_disk_measures(self):
        return self._list_measures('disk')


    def update(self):
        data = self.data['data']
        last_update = self.data['last_update']
        now = datetime.datetime.now()
        diff = now - last_update
        five_minutes = datetime.timedelta(minutes=5)
        if diff < five_minutes:
            return
        data_key = (now.day, now.month, now.year)
        
        if not data_key in data:
            data[data_key] = {}

        old_offsite_value = 0

        data[data_key]['disk'] = self.get_disk_data()

        self.data['last_update'] = now
        self._remove_old_entries()
        self.save(self.data)

    def _remove_old_entries(self):
        with self.lock:
            data = self.data['data']
            days = sorted(data, key=_sort_key_function)
            num_days = len(days)
            if num_days > self.MAX_DAYS:
                extra = days[:-self.MAX_DAYS]
                for day in extra:
                    del data[day]



def update_disk_graph():
    data_manager = GraphDataManager()
    data_manager.update()
