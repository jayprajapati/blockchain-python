import socket,threading,sys,time
from random import randint
from block import *
import json,requests
global SERVER
global PORT
mbc=blockchain(name='j',node="1923168686",port="2158")
#print(mbc)

class Server():
	
	connections=[]
	peers=[]
	vals=[]
	def __init__ (self):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		sock.bind(('127.0.0.1',10000))
		sock.listen(1)
		print("Server running ... ")
		SERVER='127.0.0.1'
		PORT=10000
		while True:
			
			c,a =sock.accept()
			cThread=threading.Thread(target=self.handler,args=(c,a))
			cThread.daemon=True
			cThread.start()
			self.connections.append(c)
			self.peers.append(a[0])
			print(str(a[0]) + ':' + str(a[1]) + " Connected!")
			self.sendPeers()
			#self.print_all()
			#sock.sendall("welcome".encode())

	def handler(self,c,a):
		while True:
			data=c.recv(1024)
			if not data:
				print(str(a[0]) + ':' + str(a[1])+ "disconnected")
				self.connections.remove(c)
				self.peers.remove(a[0])
				self.vals.remove(temp)
				
				c.close()
				self.sendPeers()
				break
			if data.decode()[:8]=="code-121":
				#print("yeyeye")
				temp=data.decode()[8:]
				if temp not in self.vals:
					self.vals.append(temp)
			if data.decode()=="printvals":
				self.print_vals()


			for connection in self.connections:
				if data.decode()=="mycmd":

					connection.send(bytes("code-120","utf-8"))
				else:
					connection.send(data)
					#connection.send(data,('127.0.0.1',10000))

			

	def sendPeers(self):
		p=""
		for peer in self.peers:
			p=p+peer + " , "

		for connection in self.connections:
			connection.send(b'\x11' + bytes(p,'utf-8'))
	
	def print_all(self):
		print("Peers list")
		for peer in self.peers:
			print(str(peer))
		print("List of conenections")
		for con in self.connections:
			print(str(con))


	def print_vals(self):
		for i in self.vals:
			print(str(i)+ "\n")



	

class Client:
	
	pairs=[]
	def sendMsg(self,sock):
		while True:
			cmd=input("enter command=")
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
			elif cmd=="x":
				self.printPeers()
			elif cmd=="pairs":
				print(self.pairs)

			else:	
				sock.send(bytes(cmd,'utf-8'))



	def __init__(self,address):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((address,10000))
		sock.send(bytes("mycmd","utf-8"))
		iThread=threading.Thread(target=self.sendMsg,args=(sock,))
		
		iThread.daemon=True
		
		iThread.start()
		self.update_node(sock)
		#self.update_node()
		while True:
			#self.update_node(sock)
			data=sock.recv(1024)
			if not data:
				break
			if data[0:1]==b'\x11':
				self.updatePeers(data[1:])

			if data.decode()=="code-120":
				#print("code-120 detected")
				try:
					sock.send(bytes("code-121|"+ str(sock.getsockname()) + "|" + str(mbc.gl()) ,'utf-8'))
					
				except:
					print("error")
					pass
			else:
				print(str(data,'utf-8'))
			print("\n")
			#print("thisis actula data= " + str(data))
			if data.decode()[:13]=="param.lenght=":
				temp=data[14:]


			

	def update_node(self,sock):
		a=mbc.gl()

		#x=str(sock.getsockname())
		
		#print(sock.getsockname())
		y="Update wave from :"+ str(sock.getsockname())+ "| lenght->" + str(a) + "\n"
		sock.send(bytes(y,"utf-8"))
		


	def updatePeers(self,peerData):
		p2p.peers=str(peerData,"utf-8").split(",")[:-1]
		
		return None

	def printPeers(self):
		for i in p2p.peers:
			print("\n" + str(i))
		print("------------------------------")
		for j in p2p.lens:
			print("\n" + str(j))
		

	

	

class p2p:
	peers=['127.0.0.1']
	lens=[]

	
while True:
	try:

		print("Trying to connect...")
		time.sleep(2)
		for peer in p2p.peers:
			try:
				client=Client(peer)
			except KeyboardInterrupt:
				sys.exit(0)
			except:
				pass
			mynum=randint(1,5)
			print(mynum)
			if mynum==3:
				try:
					server=Server()
				except KeyboardInterrupt:
					sys.exit(0)
				
			
	except KeyboardInterrupt:
		sys.exit(0)
