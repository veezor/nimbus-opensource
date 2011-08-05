#!/usr/bin/env python
import time
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
