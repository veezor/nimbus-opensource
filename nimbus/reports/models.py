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
import socket
import fileinput

from django.db import models
from django.conf import settings
from django.core.mail import send_mail as django_send_email


from nimbus.shared.fields import check_domain
from nimbus.libs.template import render_to_string
from nimbus.bacula.models import Job
from nimbus.computers.models import Computer
from nimbus.base.models import SingletonBaseModel as BaseModel

EMAIL_TEST_SUBJECT=u"Nimbus: Email de teste"
EMAIL_TEST_MESSAGE=u"""
Este email foi enviado a seu pedido para verificação da configuração de email do Nimbus.
"""
DEFAULT_SOCKET_TIMEOUT=10



FIELD_RE = ":\s*(.*)"

REPORT_EXTRA_FIELDS = [
    "Rate",
    "Software Compression",
    "Encryption"
]


class EmailConf(BaseModel):
    active = models.BooleanField(u"Ativo",default=False)
    send_to = models.EmailField(u"Enviar para",max_length=255)
    email_host = models.CharField(u"Host", max_length=255,
                                  validators=[check_domain])
    email_port = models.IntegerField(u"Porta")
    email_user = models.CharField(u"Nome do usuário",max_length=255,
                                  blank=True, null=True)
    email_password = models.CharField(u"Senha",max_length=255,
                                      blank=True, null=True)
    tls_support =  models.BooleanField(u"TLS",default=False)

    class Meta:
        verbose_name = u"Configuração de email"



def send_email(subject, message):
    conf = EmailConf.get_instance()
    settings.EMAIL_HOST = conf.email_host
    settings.EMAIL_PORT = conf.email_port
    if conf.email_user and conf.email_password:
        settings.EMAIL_HOST_USER = conf.email_user
        settings.EMAIL_HOST_PASSWORD = conf.email_password
        settings.EMAIL_USE_TLS = conf.tls_support

    if conf.active:
        socket.setdefaulttimeout(DEFAULT_SOCKET_TIMEOUT)
        django_send_email(subject, message, conf.email_user, [conf.send_to])


def send_hello_message():
    send_email(EMAIL_TEST_SUBJECT, EMAIL_TEST_MESSAGE)


def get_field_from_txt(field_name, txt):
    expr = re.compile( field_name + FIELD_RE )
    return expr.findall(txt)[0]



def get_report_extra_fields(txt):
    result = {}
    for field in REPORT_EXTRA_FIELDS:
        try:
            field_value = get_field_from_txt(field, txt)
        except IndexError:
            field_value = u'Não disponível'

        result[field] = field_value


    return result


def get_stdin():
    lines = []
    for line in fileinput.input(files="-"):
        lines.append(line)

    return "".join(lines)



def _is_self_backup(job):
    computer = job.client.computer
    nimbus_pc = Computer.objects.get(id=1)
    return computer == nimbus_pc



def send_email_report(job_id):


    conf = EmailConf.get_instance()
    if not conf.active:
        return

    job = Job.objects.get(jobid=job_id)


    if _is_self_backup(job):
        # ignore reports of self backup
        return

    procedure = job.procedure
    computer = procedure.computer

    stdin = get_stdin()
    extra_fields = get_report_extra_fields(stdin)

    fields = {
        "computer" : computer,
        "procedure" : procedure,
        "job" : job,
        "rate" : extra_fields["Rate"],
        "compression" : extra_fields["Software Compression"],
        "encryption" : extra_fields["Encryption"],
        "stdin" : stdin
    }
    message = render_to_string("email_report", **fields)
    subject = render_to_string("subject", **fields).strip()
    send_email(subject, message)
