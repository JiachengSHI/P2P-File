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
		server9 = server.Server(self.pid, self.neighbor)
		server9.start()
		#start pushupdate (details in pushupdate.py module)
		pushupdate9 = pushupdate.Pushupdate(self.pid, self.neighbor)
		pushupdate9.start()
		#start client (details in client.py module)
		client9 = client.Client(self.pid, self.neighbor)
		client9.start()
		

def main():
	#read user's choice about the topology (details in config.py module)
	topology = raw_input('choose topology (star or mesh): ')
	#start peer (peer inital)
	p9 = Peer(9, config.dict[topology]['p9'])

if __name__ == "__main__":
	main()