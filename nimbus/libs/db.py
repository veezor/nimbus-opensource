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



from django.db import models, transaction

class Session(object):

    def __init__(self, rollback_on_exception=True, 
                 commit_on_exit = True, db=None):
        self.models_to_delete_on_rollback = set()
        self.models_to_save_on_rollback = set()
        self.rollback_on_exception = rollback_on_exception
        self.db = db
        self.commit_on_exit = commit_on_exit

    def add(self, model):
        if not isinstance(model, models.Model):
            raise TypeError("models.Model is required")
        self.models_to_delete_on_rollback.add(model)

    def cancel(self, model):
        if not isinstance(model, models.Model):
            raise TypeError("models.Model is required")
        self.models_to_delete_on_rollback.discard(model)
        self.models_to_save_on_rollback.discard(model)

    def delete(self, model):
        if not isinstance(model, models.Model):
            raise TypeError("models.Model is required")
        return self.models_to_save_on_rollback.add(model)

    def __len__(self):
        return len(self.models_to_delete_on_rollback.\
                   union(self.models_to_save_on_rollback))

    def __iter__(self):
        return iter(self.models_to_delete_on_rollback.\
                    union(self.models_to_save_on_rollback))

    def __contains__(self, model):
        return model in self.models_to_delete_on_rollback.\
                    union(self.models_to_save_on_rollback)

    def clear(self):
        self.models_to_delete_on_rollback.clear()
        self.models_to_save_on_rollback.clear()

    def as_list(self):
        return list(self.models_to_delete_on_rollback.\
                    union(self.models_to_save_on_rollback))

    def commit(self):
        transaction.commit()
        self.commit_on_exit = False

    def rollback(self):
        for model in self.models_to_delete_on_rollback:
            try:
                model.delete()
            except AssertionError, error:
                #delete no-salved objects add to session
                pass
        for model in self.models_to_save_on_rollback:
            model.save()
        transaction.rollback()
        self.commit_on_exit = False

    def open(self):
        transaction.enter_transaction_management(using=self.db)
        transaction.managed(True, using=self.db)

    def close(self):
        transaction.leave_transaction_management(using=self.db)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and self.rollback_on_exception:
            self.rollback()
        if self.commit_on_exit:
            self.commit()
        self.close()
