# -*- coding:utf-8 -*-

__author__ = 'JiangHE'

'''
Count your code 
Default: Count py files in current dir(if not assign filetype and dir)
Usage: countcode.py filetype dir
'''

# Create time   : 2016-03-29 15:13:11
# Last modified : 2016-04-05 16:18:54
#########################################################

import os, sys

class CountCode:
	def __init__(self, line=0, filetype='py', dirs=os.getcwd()):
		self.line = line
		self.filetype = filetype
		self.dirs = dirs

	# Including subdirectories
	def recurCount(self):
		fnum = 0
		tlen = len(self.filetype)

		try:
			subdirs = os.listdir(self.dirs)
		except WindowsError:
			print 'Please check your directory name !'
			sys.exit()

		print '[',self.dirs,
		print "including %d subdirectories" % len(subdirs),']'
		for (thisdir, subshere, fileshere) in os.walk(self.dirs):
			for fname in fileshere:
				path = os.path.join(thisdir, fname)
#				bname = os.path.basename(path)
#				if bname[-tlen:]==self.filetype:
				if path[-tlen:]==self.filetype:
					fnum += 1
					file = open(path)
					while(file.readline()):
						self.line += 1
					file.close()
		print 'There are %d %s files' % (fnum, self.filetype)
		print "And %d lines code there, including comments" % self.line
			
	# Only Traverse current directory
	def directCount(self):
		tlen = len(self.filetype)
		try:
			L = os.listdir(self.dirs)
		except WindowsError:
			print 'Please check your directory name !'
			sys.exit()
		print '[',self.dirs,']'
		filelist = [f for f in L if f[-tlen:]==self.filetype]
		print 'There are %d %s files' % (len(filelist), self.filetype)
		os.chdir(self.dirs)
		for f in filelist:
			file = open(f)
			while(file.readline()):
				self.line += 1
			file.close()
		print "And %d lines code there, including comments" % self.line


if __name__ == '__main__':
	if len(sys.argv) > 2:
		ft = sys.argv[1]
		fd = sys.argv[2]
		count = CountCode(filetype=ft, dirs=fd)
	else:
		count = CountCode()

	count.recurCount()
	count.line = 0
	count.directCount()
