# This is hitresponse.py file
import socket
import threading

class Hit(threading.Thread):
	def __init__(self, msg, mid):
		#inital hitresponse thread parameter
		threading.Thread.__init__(self)
		self.msg = msg
		self.mid = mid

	def response(self):
		#send response directly to original peer
		self.s = socket.socket()
		self.host = socket.gethostname()
		self.port = int(self.mid.split('|')[1])

		self.s.connect((self.host, self.port))
		self.s.send(self.msg)
		self.s.close()
		print 'send hitresponse to ' + self.mid

	def run(self):
		self.response()