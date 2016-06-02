import os
import sys
# -*- coding:utf-8 -*-

__author__ = "JiangHE"

'''
Count your code 
Usage: code_counter.py filetype dir
Default: Count py files in current dir(if not assign filetype and dir)
'''

# Create time   : 2016-03-29 15:13:11
# Last modified : 6/3/2016 12:36:54 AM
#########################################################


class CountCode:
    paths = os.getcwd()

    def __init__(self, line=0, directory=paths, ftype='py'):
        self.lines = line
        self.dirs = directory
        self.fileType = ftype

    # Including subdirectories
    def recur_counter(self):
        file_num = 0
        try:
            sub_dirs = os.listdir(self.dirs)
        except WindowsError:
            print 'Please check your directory name !'
            sys.exit()
        print '\n[' + self.dirs + ']',
        print "including %d subdirectories" % len(sub_dirs)
        for (root, dis, name) in os.walk(self.dirs):
            for filename in name:
                if self.fileType in filename:
                    file_num += 1
                    with open(os.path.join(root, filename)) as f:
                        while f.readline():
                            self.lines += 1
        print 'Totally, %d %s files.' % (file_num, self.fileType)
        print "And %d lines code, including comments" % self.lines

    # Only Traverse current directory
    def direct_counter(self):
        self.lines = 0
        try:
            files = os.listdir(self.dirs)
        except WindowsError:
            print 'Please check your directory name !'
            sys.exit()
        print '\n[' + self.dirs + ']'
        file_list = [f for f in files if self.fileType in f]
        print 'Totally, %d %s files.' % (len(file_list), self.fileType),
        print 'Do not include subdirectories'
        os.chdir(self.dirs)
        for item in file_list:
            with open(item) as f:
                while f.readline():
                    self.lines += 1
        if len(file_list) != 0:
            print "And %d lines code, including comments" % self.lines


if __name__ == '__main__':
    if len(sys.argv) > 2:
        filetype = sys.argv[1]
        dirs = sys.argv[2]
        counter = CountCode(ftype=filetype, directory=dirs)
    else:
        counter = CountCode()

    counter.recur_counter()
    counter.direct_counter()
