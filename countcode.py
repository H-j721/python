# -*- coding:utf-8 -*-

__author__ = 'JiangHE'

'''
Count your code 
Usage: countcode.py filetype dir
'''

# Create time   : 2016-03-29 15:13:11
# Last modified : 2016-04-05 14:08:22
#########################################################

import os, sys

class CountCode:
	def __init__(self, line=0, filetype='py', dirs=os.chdir(os.getcwd())):
		self.line = line
		self.filetype = filetype
		self.dirs = dirs
	def lister(self):
		fnum = 0
		print self.dirs
#		os.chdir(self.dirs)
		tlen = len(self.filetype)
		for (thisdir, subshere, fileshere) in os.walk(self.dirs):
#			print '['+thisdir+']'
			for fname in fileshere:
				path = os.path.join(thisdir, fname)
				bname = os.path.basename(path)
#				print path
				if bname[-tlen:]==self.filetype:
					fnum += 1
					file = open(path)
					while(file.readline()):
						self.line += 1
					file.close()
		print 'There are %d %s files in %s' % (fnum, self.filetype, self.dirs)
		print "And %d lines code there, including comments" % self.line
			
	def count(self):
		L = os.listdir(self.dirs)
		filelist = [f for f in L if f[-tlen:]==self.filetype]
		print 'There are %d %s files in %s' % (len(filelist), self.filetype, self.dirs)
		os.chdir(self.dirs)
		for f in filelist:
			file = open(f)
			while(file.readline()):
				self.line += 1
			file.close()
		print "And %d lines code there, including comments" % self.line

if __name__ == '__main__':
	ft = sys.argv[1]
	fd = sys.argv[2]
	count = CountCode(filetype=ft, dirs=fd)
	count.lister()
