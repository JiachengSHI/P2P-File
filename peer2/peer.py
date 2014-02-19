# This is peer.py file
import server
import client
import pushupdate
import config
import rw

class Peer:
	def __init__(self, pid, neighbor):
		#define the peer id & its neighbor
		self.pid = pid
		self.neighbor = neighbor
		#inital msg_list & req_list file
		rw.writeFile('msg_list.txt', '')
		rw.writeFile('req_list.txt', '')
		#start server thread (details in server.py module)
		server2 = server.Server(self.pid, self.neighbor)
		server2.start()
		#start pushupdate (details in pushupdate.py module)
		pushupdate2 = pushupdate.Pushupdate(self.pid, self.neighbor)
		pushupdate2.start()
		#start client (details in client.py module)
		client2 = client.Client(self.pid, self.neighbor)
		client2.start()
		

def main():
	#read user's choice about the topology (details in config.py module)
	topology = raw_input('choose topology (star or mesh): ')
	#start peer (peer inital)
	p2 = Peer(2, config.dict[topology]['p2'])

if __name__ == "__main__":
	main()