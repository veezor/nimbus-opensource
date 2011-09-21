#!/usr/bin/env python

import os
import sys
import commands

GIT_LAST_HASH_COMMAND = "git rev-parse HEAD"


class Bumper(object):

    def __init__(self, version_file, debian_control_file):
        self.version_file = version_file
        self.debian_control_file = debian_control_file
        self.major = None
        self.minor = None
        self.patch_level = None
        self.git_hash = None

    def read_version(self):
        with file(self.version_file) as f:
            content = f.read().strip()
        
        content = content.split('-')[0].split('.') # major.minor.patch_level hash
        self.major = int(content[0])
        self.minor = int(content[1])
        self.patch_level = int(content[2])

        self.git_hash = self.get_git_hash()


    def version_to_string(self):
        version = "%s.%s.%s" % (self.major, self.minor, self.patch_level)

        if self.git_hash:
            version += ("-%s" % self.git_hash)

        return version


    def write_version(self):
        self._write_debian_control_file()

        with file(self.version_file, "w") as f:
            f.write(self.version_to_string())


    def _write_debian_control_file(self):

        with file(self.debian_control_file) as f:
            lines = f.readlines()

        for index,line in enumerate(lines):
            if line.startswith('Version'):
                break

        lines[index] = 'Version: %s\n' % self.version_to_string()

        with file(self.debian_control_file, "w") as f:
            f.writelines(lines)




    def get_git_hash(self):
        status, output = commands.getstatusoutput(GIT_LAST_HASH_COMMAND)
        if status != 0:
            return None
        else:
            return output

    def next_patch_level(self):
        self.patch_level += 1

    def next_minor(self):
        self.minor += 1
        self.patch_level = 0

    def next_major(self):
        self.major += 1
        self.minor = 0
        self.patch_level = 0

    def __enter__(self):
        self.read_version()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.write_version()



def usage():
    print 'usage: bump.py [options] version_file debian_control_file'
    print 'options:'
    print '\t--major: increment major version'
    print '\t--minor: increment minor version'
    print '\t--patch_level: increment patch_level version'
    print '='* 20
    print 'if BUMP_VERSION_FILE is defined, then version_file=BUMP_VERSION_FILE'
    print 'if BUMP_DEBIAN_CONTROL_FILE is defined, then debian_control_file=BUMP_DEBIAN_CONTROL_FILE'
    sys.exit(1)



def main():
    try:
        param = sys.argv[1]

        try:
            version_file = os.environ['BUMP_VERSION_FILE']
        except KeyError:
            version_file = sys.argv[2]

        try:
            debian_control_file = os.environ['BUMP_DEBIAN_CONTROL_FILE']
        except KeyError:
            debian_control_file = sys.argv[3]


        if param == '--minor':
            with Bumper(version_file, debian_control_file) as b:
                b.next_minor()
        elif param == '--major':
            with Bumper(version_file, debian_control_file) as b:
                b.next_major()
        elif param == '--patch-level':
            with Bumper(version_file, debian_control_file) as b:
                b.next_patch_level()
        elif param == '--update-git-hash':
            with Bumper(version_file, debian_control_file) as b:
                pass
        else:
            usage()

    except IndexError:
        usage()

if __name__ == "__main__":
    main()
