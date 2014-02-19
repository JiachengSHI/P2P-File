# This is pushupdate.py file
import os
import sys
import time
import threading

import autobroadcast
import rw

class Pushupdate(threading.Thread):
	def __init__(self, pid, neighbor):
		#inital pushupdate thread parameter
		threading.Thread.__init__(self)
		#scan all the original file
		self.fileinfo = self.scan()
		self.index = self.fileinfo[0]
		self.ct = self.fileinfo[1]
		self.lmt = self.fileinfo[2]
		#read file metadata from metadata.txt
		self.meta_dict = rw.readDict('metadata.txt')['original']
		
		self.pid = pid
		self.port = 2222 + self.pid * 10
		self.neighbor = neighbor
		self.msgid = 0

	def scan(self):
		path = os.path.join(os.getcwd(), 'files', 'original')
		index = os.listdir(path)
		#scan files in the index, including crate time & last modified time
		for f in index:
			ct = [os.path.getctime(os.path.join(path,f))]
			lmt = [os.path.getmtime(os.path.join(path,f))]
		return index, ct, lmt

	def monitor(self):
		nfileinfo = self.scan()
		nindex = nfileinfo[0]
		nct = nfileinfo[1]
		nlmt = nfileinfo[2]
		#check if the file has been delete or replaced or added
		if nct != self.ct or nindex != self.index:
			print 'files have been replaced!'
		else:
			if nlmt != self.lmt:
				for i in range(0, len(nlmt)):
					if nlmt[i] != self.lmt[i]:
						filename = nindex[i]
						print '%s has been modified!' % filename
						#update version number & last modified time in metadata file.
						self.meta_dict[filename]['version'] += 1
						self.meta_dict[filename]['LMT'] = nlmt[i]
						meta_dict = rw.readDict('metadata.txt')
						meta_dict['original'] = self.meta_dict
						rw.write('metadata.txt', meta_dict)
						self.push(filename, self.meta_dict[filename]['version'])
					i += 1
				#update the variable last modified time after each push.
				self.lmt = nlmt
			else:
				print 'everything is unchanged!'
				print nfileinfo

	def push(self, name, version):
		#send update msg to all peers
		self.msgid += 1
		msg = 'mid:' + str(self.pid) + '|' + str(self.port) + '|update|' + str(self.msgid) + ',update:' + name + ',version:' + str(version)
		mid = msg.split(',')[0].split(':')[1]
		#read mid_list from file 'msg_list'
		mid_list = rw.readList('msg_list.txt')
		#update mid_list
		mid_list.append(mid)
		rw.write('msg_list.txt', mid_list)
		broadcast = autobroadcast.Auto(msg, self.neighbor)
		broadcast.start()
		broadcast.join()

	def run(self):
		while True:
			print 'monitoring ...'
			self.monitor()
			time.sleep(10.0)