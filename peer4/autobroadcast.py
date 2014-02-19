# This is autobroadcast.py file
import socket
import threading

class Auto(threading.Thread):
	def __init__(self, msg, neighbor):
		#inital autobroadcast thread parameter
		threading.Thread.__init__(self)
		self.msg = msg
		self.neighbor = neighbor

	def broadcast(self):
		#broadcast message to all neighbor
		for n in self.neighbor:
			self.s = socket.socket()
			self.host = socket.gethostname()
			self.port = 2222 + 10 * n
			self.s.connect((self.host, self.port))
			self.s.send(self.msg)
			self.s.close()
		print 'broadcast message'

	def run(self):
		self.broadcast()