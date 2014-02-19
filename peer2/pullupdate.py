# This is pullupdate.py file
import os
import time
import threading

import hitresponse
import rw

class Pullupdate(threading.Thread):
	def __init__(self, pid):
		#inital pullupdate thread parameter
		threading.Thread.__init__(self)
		self.pid = pid
		self.port = 2222 + self.pid * 10

	def monitor(self):
		#check all download files, see if it's TTR Expired or not
		Dict = rw.readDict('metadata.txt')
		if 'download' in Dict.keys():
			meta_dict = Dict['download']
			count = [y for x,y in meta_dict.items()]
			for i in range(0, len(count)):
				if count[i]['state'] == 'valid':
					if time.time() >= count[i]['TTR'] + count[i]['LMT']:
						#alarm user file is TTR Expired
						count[i]['state'] = 'TTR Expired'
						filename = meta_dict.keys()[i]
						print '%s is expired, need to refresh' % filename
						#let user choose to update ot not
						cmd = raw_input('update or not ? (yes/no) : ')
						if cmd == 'yes':
							self.pull(filename, meta_dict[filename])
						else:
							pass
				i += 1
		else:
			pass

	def pull(self, name, metadata):
		#send check response to the original peer
		msg = 'mid:' + str(self.pid) + '|' + str(self.port) + ',check:' + name + ',version:' + str(metadata['version']) + ',TTR:' + str(metadata['TTR'])
		mid = metadata['mid']
		hit = hitresponse.Hit(msg, mid)
		hit.start()
		hit.join()

	def run(self):
		while True:
			self.monitor()
			time.sleep(10.0)