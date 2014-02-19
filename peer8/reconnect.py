# This is reconnect.py file
import os
import json
import socket
import threading

import rw

class Connect(threading.Thread):
	def __init__(self, msg, mid, name):
		#inital reconnect thread parameter
		threading.Thread.__init__(self)
		self.msg = msg
		self.mid = mid
		self.name = name

	def reconn(self):
		#reconnect to response peer
		self.s = socket.socket()
		self.host = socket.gethostname()
		self.port = int(self.mid.split('|')[1])
		
		self.s.connect((self.host, self.port))
		print 'reconnect to ' + self.mid
		self.s.send(self.msg)
		#download metadata & file from response peer
		metadata = json.loads(self.s.recv(1024))
		#download file by chunks
		i = 0
		content = ''
		while i != 1:
			chunk = self.s.recv(1024)
			if len(chunk) == 0:
				i = 1
			else:
				content += chunk
		self.s.close()
		path = os.path.join(os.getcwd(), 'files', 'download', self.name)
		rw.writeFile(path, content)
		#read name_list from file 'req_list'
		name_list = rw.readList('req_list.txt')
		#update name_list
		name_list.remove(self.name)
		rw.write('req_list.txt', name_list)
		#update metadata
		meta_dict = rw.readDict('metadata.txt')
		if 'download' in meta_dict.keys():
			meta_dict['download'][self.name] = metadata
		else:
			file_dict = {}
			file_dict[self.name] = metadata
			meta_dict['download'] = file_dict
		rw.write('metadata.txt', meta_dict)
		print 'receive file: ' + self.name

	def run(self):
		self.reconn()