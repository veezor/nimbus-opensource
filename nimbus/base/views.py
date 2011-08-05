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
# Create your views here.

import operator

import systeminfo

import re

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from nimbus.shared import utils, middlewares
from nimbus.shared.views import render_to_response
from nimbus.shared.utils import block_ie_browser
from nimbus.bacula.models import Job
from nimbus.libs import graphsdata

from nimbus.procedures.models import Procedure
from nimbus.computers.models import Computer


@login_required
def home(request):
    job_bytes = Job.get_bytes_from_last_jobs()
    table1 = {
        'title': u"Quantidade de dados realizados backup", 'width': "100%",
        'type': "bar",
        'cid': "chart1",
        'header': [d.strftime("%d/%m/%y") for d in sorted(job_bytes)],
        'labels': [utils.filesizeformat(v) for k, v in sorted(job_bytes.items())],
        'lines': {
            "Dados": utils.ordered_dict_value_to_formatted_float(job_bytes)
        }
    }

    job_files = Job.get_files_from_last_jobs()
    table2 = {
        'title': u"Quantidade de arquivos realizados backup", 'width': "100%",
        'type': "bar",
        'cid': "chart2",
        'header': [d.strftime("%d/%m/%y") for d in sorted(job_files)],
        'labels': [int(v) for k, v in sorted(job_files.items())],
        'lines': {
            "Arquivos": [int(v) for k, v in sorted(job_files.items())]
        }
    }

    graphsdata.update_disk_graph()
    graph_data_manager = graphsdata.GraphDataManager()
    diskdata = graph_data_manager.list_disk_measures()
    

    table3 = {'title': u"Ocupação do disco (GB)", 'width': "", 'type': "area", 'cid': "chart3", 'height': "200",
              'header': [i[0] for i in diskdata], 'labels': [utils.filesizeformat(i[1], "GB") for i in diskdata]}
    #table3['header'] = ["Gigabytes"]
    #setando valor padrao
    t3data = [utils.filesizeformat(i[1], "GB") for i in diskdata] if len(diskdata) else [0.0]
    table3['lines'] = {"Disponível": t3data}


    memory = systeminfo.get_memory_usage()
    memory_free = 100 - memory

    table4 = {'title': u"Uso da memória", 'width': "90%", 'type': "pie", 'cid': "chart4", 'header': ["Gigabytes"],
              'lines': {
                  "Disponível": [memory_free],
                  "Ocupado": [memory]}}

    cpu = systeminfo.get_cpu_usage()
    cpu_free = 100 - memory


    table5 = {'title': u"Uso da CPU", 'width': "", "type": "pie", 'cid': "chart5", 'header': ["Clocks"], 'lines': {
        "Disponível": [cpu_free],
        "Ocupado": [cpu]}}


    # Dados de content:
    # - type
    # - label
    # - date
    # - message

    last_jobs = Procedure.all_jobs()[:5]

    return render_to_response(request, "home.html", locals())

def ie_error(request):
    return render_to_response(request, "ie_error.html", locals())
    
def license(request):
    return render_to_response(request, "license_general.html", locals())



