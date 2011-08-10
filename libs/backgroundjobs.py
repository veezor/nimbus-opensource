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



import logging
import types
from threading import RLock, Thread
from datetime import datetime
from functools import wraps
from Queue import Queue



(MAX_PRIORITY,
 NORM_PRIORITY,
 MIN_PRIORITY) = range(3)



def synchronized(method):

    @wraps(method)
    def sync_method(self, *args, **kwargs):
        with self.rlock:
            return method(self, *args, **kwargs)


    return sync_method





class Job(object):

    jobid = 0
    classlock = RLock()

    def __init__(self, description, priority, 
                       callback, *args, **kwargs):
        super(Job, self).__init__()
        self.rlock = RLock()
        self.id = self.get_next_jobid()
        self.description = description
        self.priority = priority
        self.callback = callback
        self.args = args
        self.pending = True
        self.kwargs = kwargs
        self.created_at = datetime.now()


    def invoke(self):
        rvalue = self.callback(*self.args, **self.kwargs)
        self.pending = False
        return rvalue

    @property
    @synchronized
    def status(self):
        if self.pending:
            return "processing"
        else:
            "finished"

    @classmethod
    def get_next_jobid(cls):
        with cls.classlock:
            cls.jobid += 1
            return cls.jobid



NullJob = Job("Null job", MAX_PRIORITY, lambda : None) # signal for workerthread stop


def min_priority_job(description, callback, *args, **kwargs):
    return Job(description, MIN_PRIORITY, 
               callback, *args, **kwargs)


def norm_priority_job(description, callback, *args, **kwargs):
    return Job(description, NORM_PRIORITY, 
               callback, *args, **kwargs)


def max_priority_job(description, callback, *args, **kwargs):
    return Job(description, MAX_PRIORITY, 
               callback, *args, **kwargs)


class WorkerThread(Thread):

    def __init__(self):
        super(WorkerThread, self).__init__()
        self.rlock = RLock()
        self.jobs = set()
        self.queue = Queue()
        self.has_stopped = False
        self._heavyweight_jobs = 0
        self.logger = logging.getLogger(self.getName())
        self.logger.info("worker thread initialized")


    @synchronized
    def add_job(self, job):
        self.jobs.add( job )
        self.queue.put( job )

        if job.priority == MIN_PRIORITY:
            self._heavyweight_jobs += 1

        self.logger.info("Add to %s WorkerThrad" % \
                (job.description))

    @synchronized
    def get_num_heavyweight_jobs(self):
        return self._heavyweight_jobs


    @synchronized
    def get_jobs(self):
        return list(self.jobs)


    @synchronized
    def get_num_jobs(self):
        return len(self.get_jobs())

    @synchronized
    def stop(self):
        self.has_stopped = True
        self.add_job( NullJob )


    def run(self):
        while not self.has_stopped:
            try:
                self.logger.info("worker thread trying get something")
                job = self.queue.get()
                self.logger.info("worker thread invoking")
                job.invoke()
                self.remove_job(job)
                self.logger.info("worker thread get and call sucessful")
            except Exception, error:
                self.remove_job(job)
                self.logger.exception("Error in callable on workerthread")


    @synchronized
    def remove_job(self, job):
        self.jobs.remove(job)
        if job.priority == MIN_PRIORITY:
            self._heavyweight_jobs -= 1



class ThreadPool(object):
    

    def __init__(self, num_workers=5):
        super(ThreadPool, self).__init__()
        self.num_workers = num_workers
        self.rlock = RLock()
        self.workers = []


    @synchronized
    def _start_new_worker(self):
        if len(self.workers) < self.num_workers:
            worker = WorkerThread()
            worker.start()
            self.workers.append(worker)
            return worker


    @synchronized
    def add_job(self, job):

        active_workers = len(self.workers)

        if not self.workers:
            self._start_new_worker()

        workers_state_busy = [ w.get_num_heavyweight_jobs() for w in self.workers ]


        if all(workers_state_busy):

            if active_workers == self.num_workers:
                best_worker = sorted(self.workers, 
                                     key=lambda w: (w.get_num_heavyweight_jobs(), 
                                                    w.get_num_jobs()))[0]
                best_worker.add_job(job)
            else:
                worker = self._start_new_worker()
                worker.add_job( job )

        else:
            workers = [ w for w in self.workers if w.get_num_heavyweight_jobs() == 0 ]
            best_worker = sorted(workers, 
                                 key=lambda w: w.get_num_jobs())[0]
            best_worker.add_job(job)


    @synchronized
    def has_job_pending(self, jobid):
        jobs = self.list_jobs_pending()
        return jobid in [ job.id for job in jobs  ]

    @synchronized
    def list_jobs_pending(self):
        result = []
        for worker in self.workers:
            result.extend( worker.get_jobs() )
        return result

