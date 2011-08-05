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



from django.conf.urls.defaults import *

urlpatterns = patterns('nimbus.restore.views',
    (r'^(?P<object_id>\d+)/view/$', 'view'), 
    (r'^view/$', 'view'), 
    (r'^restore_files', 'restore_files'),
    (r'^get_tree/$', 'get_tree'),
    (r'^get_client_tree/$', 'get_client_tree'),
    (r'^get_procedures/(?P<object_id>\d+)/', 'get_procedures'),
    (r'^get_jobs/(?P<procedure_id>\d+)/(?P<data_inicio>.*?)/(?P<data_fim>.*?)/', 'get_jobs'),
    (r'^get_tree_search_file/$', 'get_tree_search_file'),
)
