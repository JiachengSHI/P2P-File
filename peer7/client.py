# This is client.py file
import os
import sys
import socket
import threading
import json

import rw

class Client(threading.Thread):
	def __init__(self, pid, neighbor):
		#initial client parameter
		threading.Thread.__init__(self)
		self.pid = pid
		self.neighbor = neighbor
		self.msgid = 0
		while True:
			self.commend()

	def commend(self):
		#read user's commend from cmd
		cmd = raw_input('Enter commend here: ')
		if cmd == "exit":
			sys.exit(0)
		elif cmd == "obtain":
			self.msgid += 1
			filename = raw_input('Enter filename: ')
			self.obtain(filename)
			self.commend()

	def obtain(self, filename):
		#define message
		msg = 'mid:' + str(self.pid) + '|' + str(2222 + self.pid * 10) + '|' + str(self.msgid) + ',search:' + filename + ',TTL=10'
		mid = msg.split(',')[0].split(':')[1]
		#read mid_list from file 'msg_list'
		mid_list = rw.readList('msg_list.txt')
		#update mid_list
		mid_list.append(mid)
		rw.write('msg_list.txt', mid_list)
		#read name_list from file 'req_list'
		name_list = rw.readList('req_list.txt')
		#update name_list
		name_list.append(filename)
		rw.write('req_list.txt', name_list)
		#broadcast message to its neighbor
		for n in self.neighbor:
			self.s = socket.socket()
			self.host = socket.gethostname()
			self.port = 2222 + 10 * n
			print 'connect port: ' + str(self.port)
			self.s.connect((self.host, self.port))
			self.s.send(msg)
			self.s.close()
		print 'searching... ...'