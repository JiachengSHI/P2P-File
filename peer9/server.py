# This is server.py file
import os
import sys
import socket
import threading
import json

import autobroadcast
import hitresponse
import reconnect
import pullupdate
import pullrenew
import rw

class Server(threading.Thread):
	def __init__(self, pid, neighbor):
		#initial server thread parameter
		threading.Thread.__init__(self)
		self.pid = pid
		self.neighbor = neighbor
		#start pullupdate (details in pullupdate.py module)
		pullupdate0 = pullupdate.Pullupdate(self.pid)
		pullupdate0.start()

	def fileindex(self, filetype):
		#read all file's name into an index from 'files' directory
		path = os.path.join(os.getcwd(),'files', filetype)
		index = os.listdir(path)
		return index

	def run(self):
		#define the server thread
		self.s = socket.socket()
		self.host = socket.gethostname()
		self.port = 2222 + self.pid * 10
		self.s.bind((self.host, self.port))
		self.s.listen(5)

		while True:
			#listen for connection
			c, addr = self.s.accept()
			print '\nGot connection from ', addr

			#initialize file index
			original_index = self.fileindex('original')
			download_index = self.fileindex('download')
			index = original_index + download_index

			#receive message
			msg = c.recv(1024)
			#parse & analyze message
			mid = msg.split(',')[0].split(':')[1]
			action = msg.split(',')[1].split(':')[0]
			name = msg.split(',')[1].split(':')[1]

			if action == 'search':
				print 'search ' + name
				ttl = msg.split(',')[2].split('=')[1]
				#read mid_list from file 'msg_list'
				mid_list = rw.readList('msg_list.txt')
				#decide broadcast or not
				if int(ttl) == 1 or mid in mid_list:
					print 'file dont need to pass'
				else:
					#update mid_list in file 'msg_list'
					mid_list.append(mid)
					rw.write('msg_list.txt', mid_list)
					#decrease the ttl value by 1 after broadcast for once
					rmsg = msg.rsplit(ttl, 1)
					msg = str(int(ttl)-1).join(rmsg)
					#start autobroadcast thread (details in autobroadcast.py module)
					broadcast = autobroadcast.Auto(msg, self.neighbor)
					broadcast.start()
					broadcast.join()
					if name in index:
						#check file's state
						meta_dict = rw.readDict('metadata.txt')
						if (name in original_index and (meta_dict['original'][name]['state'] == 'valid' or meta_dict['download'][name]['state'] == 'valid')):
							#start hitresponse thread (details in hitresponse.py module)
							msg = 'mid:' + str(self.pid) + '|' + str(self.port) + ',response:' + name
							hit = hitresponse.Hit(msg, mid)
							hit.start()
							hit.join()
						else:
							'file state is not qualified'
					else:
						print 'no file match, pass to neighbors'
			elif action == 'update':
				print 'update ' + name
				#read mid_list from file 'msg_list'
				mid_list = rw.readList('msg_list.txt')
				#decide broadcast or not
				if mid in mid_list:
					print 'update dont need to pass'
				else:
					#update mid_list in file 'msg_list'
					mid_list.append(mid)
					rw.write('msg_list.txt', mid_list)
					#start autobroadcast thread (details in autobroadcast.py module)
					broadcast = autobroadcast.Auto(msg, self.neighbor)
					broadcast.start()
					broadcast.join()
					if name in download_index:
						#set file state to invalid
						meta_dict = rw.readDict('metadata.txt')
						meta_dict['download'][name]['state'] = 'invalid'
						rw.write('metadata.txt', meta_dict)
					else:
						print 'no file need to update, pass to neighbors'
			elif action == 'check':
				print 'check ' + name
				#check the original file's version
				version = int(msg.split(',')[2].split(':')[1])
				TTR = int(msg.split(',')[3].split(':')[1])
				meta_dict = rw.readDict('metadata.txt')
				if meta_dict['original'][name]['version'] == version:
					#if same version, send a new TTR.
					newTTR = 2 * TTR
					msg = 'mid:' + str(self.pid) + '|' + str(self.port) + ',checkresponse:' + name + ',state:valid,TTR:' + str(newTTR)
				else:
					#send Invalid & new version exist.
					msg = 'mid:' + str(self.pid) + '|' + str(self.port) + ',checkresponse:' + name + ',state:invalid'
				hit = hitresponse.Hit(msg, mid)
				hit.start()
				hit.join()
			elif action == 'checkresponse':
				print 'checkresponse ' + name
				#update the metadata
				state = str(msg.split(',')[2].split(':')[1])
				if state == 'valid':
					TTR = int(msg.split(',')[3].split(':')[1])
					#change TTR to 2TTR. (details in pullrenew.py module)
					pullrenew.renew('TTR', name, TTR)
					#change state from 'TTR Expired' back to 'valid' (details in pullrenew.py module)
					pullrenew.renew('state', name, state)
				elif state == 'invalid':
					#change state from 'TTR Expired' back to 'invalid' (details in pullrenew.py module)
					pullrenew.renew('state', name, state)
			elif action == 'response':
				#start reconnect thread (details in reconnect.py module)
				print 'response ' + name + ' from ' + mid
				#read name_list from file 'req_list'
				name_list = rw.readList('req_list.txt')
				#decide reconnect or not
				if name in name_list:
					msg = 'mid:' + str(self.pid) + '|' + str(self.port) + ',obtain:' + name
					connect = reconnect.Connect(msg, mid, name)
					connect.start()
					connect.join()
				else:
					print 'file has been obtained'
			elif action == 'obtain':
				print 'obtain ' + name
				#start transfer directly to original peer
				if name in original_index:
					path = os.path.join(os.getcwd(), 'files', 'original', name)
					metadata = rw.readDict('metadata.txt')['original'][name]
				elif name in download_index:
					path = os.path.join(os.getcwd(), 'files', 'download', name)
					metadata = rw.readDict('metadata.txt')['download'][name]
				#send metadata & file
				c.sendall(json.dumps(metadata))
				#slice file into chunks by buffer
				content = rw.readFile(path)
				i = 0
				while i <= len(content):
					chunk = buffer(content, i, 1024)
					c.sendall(chunk)
					i += 1024
				print 'send file: ' + name

			c.close()