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


import os


INTERVAL = 2


class DiskInfo(object):

    def __init__(self, path):
        self.path = path


    def get_data(self):
        info = os.statvfs(self.path)
        total = info.f_bsize * info.f_blocks
        free = info.f_bsize * info.f_bfree
        used = total - free
        return total, used, free


    def get_usage(self):
        total, used, free = self.get_data()
        usage = 100 *( float(used) / total)
        return usage

    def get_used(self):
        return self.get_data()[1]




class CPUInfo(object):

    def get_data(self):
        with file("/proc/stat", "r") as stat:
            line = stat.readline()

        line = line.split()[1:7]
        line = map(int, line)
        return line


    def get_data_diff(self, interval):

        data_old = self.get_data()
        time.sleep(interval)
        data_new = self.get_data()


        diff = map(lambda x,y: y - x, data_old, data_new)

        return diff


    def get_usage(self):
        diff = self.get_data_diff(INTERVAL)
        usage = sum(diff[:3])
        usage = (100.0 * usage) / (sum(diff) or 1)
        return usage



class MemoryInfo(object):

    def get_data(self):

        with file("/proc/meminfo") as stat:
            data = stat.readlines()

        data = data[:4]
        data = map(lambda line: int(line.split()[1]), data)

        return data


    def get_usage(self):
        data = self.get_data()

        (total,
         pfree, 
         buffer,
         cache ) = data

        free = pfree + buffer + cache
        usage = total - free
        usage = (usage / float(total)) * 100
        return usage




def get_partition_usage(path):
    return DiskInfo(path).get_usage()


def get_cpu_usage():
    return CPUInfo().get_usage()


def get_memory_usage():
    return MemoryInfo().get_usage()


if __name__ == "__main__":
    info = CPUInfo()
    print info.get_usage()
    info = MemoryInfo()
    print info.get_usage()
