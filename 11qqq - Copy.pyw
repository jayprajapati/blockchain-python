import socket,threading,sys,time
from random import randint
from block import *
import json,requests
#mbc=blockchain(name='j',node="dontknow",port=1)
from newserver import *



class Server():
	
	connections=[]
	peers=[]
	lens=[]
	pairs={}
	def __init__ (self):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		sock.bind(('127.0.0.1',10000))
		sock.listen()
		print("Server running ... ")
		while True:
			
			c,a =sock.accept()
			cThread=threading.Thread(target=self.handler,args=(c,a))
			cThread.daemon=True
			cThread.start()
			self.connections.append(c)
			self.peers.append(a[0])
			print(str(a[0]) + ':' + str(a[1]) + "Connected!")
			print("sending peers ")
			self.sendPeers()
			try:
				c=connections[randint(1,len(connections))]
				c.send(bytes("code-121","utf-8"))
			except:
				print("exception passed")
				pass	


	def handler(self,c,a):
		while True:

			data=c.recv(1024)
			

			if data.decode()[0:8]=='code-120':
				#print("executed")
				if data.decode()[8:] not in self.lens:
					self.lens.append(data.decode()[8:])
					x=data.decode()[8:].split("|")
					print(x)
					tm={ x[0] : int(x[1])}
					self.pairs.update(tm)
			#self.fun_len()
			
			if data.decode()[0:8]=="code-121":
				print("requests register for code-121")
				#print(self.pairs)
				self.fun_len()
			for connection in self.connections:
				connection.send(data)
			if not data:
				print("no data found")
				print(str(a[0]) + ':' + str(a[1])+ "disconnected")
				self.connections.remove(c)
				self.peers.remove(a[0])
				print("removed all netry")
				c.close()
				self.sendPeers()
				break

	def sendPeers(self):
		p=""
		for peer in self.peers:
			p=p+peer + " , "

		for connection in self.connections:
			connection.send(b'\x11' + bytes(p,'utf-8'))

	def fun_len(self):
		best=max(self.pairs,key=self.pairs.get)
		#best=self.pairs[best]
		#all_best=[key for key in pairs.keys() if pairs[key]==best]
		#all_b=[]
		#for key in self.pairs.keys():
		#	if self.pairs[key]==best:
		#		all_b.append(key)
		print("Legit BC contains at = "+ str(best) )
		#print(best[1:-1].split(",")[0])
		node_addr=best[1:-1].split(",")[0][1:-1]
		node_port=best[1:-1].split(",")[1]
		#print(all_b)
		for connection in self.connections:
			if str(connection.getpeername())==str(best):
				connection.send(bytes("code-123","utf-8"))
		import requests
		u='http://'+node_addr+':'+str(8081)
		u=u.replace(" ","")
		print(u)
		while True:
			
			r=requests.get(u)
			if r.status_code==200:
				for connection in self.connections:
						if str(connection.getpeername())!=str(best):
							print(str(connection.getpeername()))
							print("\nbes tis =" + str(best))
							print("sendinh code-125 to " + str(connection))
							connection.send(bytes("code-125|"+str(best),"utf-8"))
				break




	

class Client:
	x=1

	def sendMsg(self,sock):
		while True:
			# if self.x==1:
			# 	print("data sent")
			# 	sock.send(bytes("code-121",'utf-8'))
			# 	self.x=self.x+1
			cmd=input("Enter Command=")
			if cmd=="showbc":
				print("\n")
				print(mbc)
			elif cmd=="getblock":
				print("\nFetching block.....")
				try:
					import requests
				except ModuleNotFoundError:
					pass
				r = requests.get('http://localhost:8000/site/block')
				r=r.json()
				for i,j in r.items():
					print("" + str(i) + " ->" + str(j))
				
				bb=block(data=r['name'],last_hash=mbc.get_last_hash())
				mbc.commit(bb.mine_block())
				print("block Mined!")
			elif cmd=="gl":
				a=mbc.gl()
				print("Lenght of bc is " + str(a))
			elif cmd=="code-121":
				sock.send(bytes(cmd,'utf-8'))
			elif cmd=="code-444":
				iThread3=threading.Thread(target=run)
				iThread3.daemon=True
				iThread3.start()



	

	def __init__(self,address):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((address,10000))
		
		
		temp=str(sock.getsockname())
		
		node_addr=temp[1:-1].split(",")[0]
		node_port=temp[1:-1].split(",")[1]
		#print("" + node_addr + " |")
		

		iThread2=threading.Thread(target=self.sendLen,args=(sock,))
		iThread2.daemon=True
		iThread2.start()

		iThread=threading.Thread(target=self.sendMsg,args=(sock,))
		iThread.daemon=True
		iThread.start()

		
		

		while True:
			data=sock.recv(1024)
			if not data:
				break
			if data[0:1]==b'\x11':
				#print("updating peers data")
				self.updatePeers(data[1:])
			if data.decode().split(" ")[0]=="msg":
				print(str(data[4:],'utf-8'))
			if data.decode()[0:8]=="code-123":
				try:
					iThread3=threading.Thread(target=run)
					iThread3.daemon=True
					iThread3.start()

				except:
					print("ysy")
			if data.decode()[0:8]=="code-125":
				ad=data.decode()[8:][1:-1].split(",")[0]
				ad=ad[2:-1]
				por=data.decode()[8:][1:-1].split(",")[1]
				print("got code-125 requests")
				try:
					import requests
					url="http://"+str(ad)+":8081"
					print(url)
					rq = requests.get('http://'+str(ad)+":"+str(8081))
					if rq.status_code==200:
						print("Replacing Current Chain....")
						rq=rq.json()
						#print(rq['blocks'])
						
						mbc.empty_bc()
						print("Empty Blockchain")
						a=rq['blocks']
						for i,j in a.items():
							print("timestamp is  = " + str(j['timestamp']))
							bb=block(data="",last_hash="")
							bb.data=j['data']
							bb.last_hash=j['last_hash']
							bb.timestamp=str(j['timestamp'])
							bb.hashvalue=j['hashvalue']
							mbc.commit(bb)
						print("Chain Successfully Replaced!")



					else:
						print("problem with link")
				except:
					print("http server error")

			#print(str(data,'utf-8'))
	def updatePeers(self,peerData):
		p2p.peers=str(peerData,"utf-8").split(",")[:-1]
		return None

	def sendLen(self,sock):
		while True:
			#print("updating len")
			temp="code-120"+str(sock.getsockname()) + "|"+ str(mbc.gl())

			sock.send(bytes(temp,"utf-8"))
			time.sleep(2)

class p2p:
	peers=['127.0.0.1']

	
while True:
	try:

		print("Trying to connect...")
		
		for peer in p2p.peers:
			try:
				client=Client(peer)
			except KeyboardInterrupt:
				sys.exit(0)
			except:
				pass
			if randint(1,4)==2:
				try:
					server=Server()
				except KeyboardInterrupt:
					sys.exit(0)

			
	except KeyboardInterrupt:
		sys.exit(0)
