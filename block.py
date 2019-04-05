import time,hashlib
import random
class block():

	def __init__(self,data,last_hash,nounce=1):
		self.timestamp=time.time()
		self.last_hash=last_hash
		self.data=data
		
		m=str(self.data)+str(self.timestamp)+str(self.last_hash)+str(nounce)
		m=m.encode('UTF-8')
		self.hashvalue=hashlib.sha256(m).hexdigest()



	def __str__(self):
		print("---------------block----------------")
		print("timestamp     : " + str(self.timestamp))
		print("last_hash     : " + str(self.last_hash))
		print("data     : " + str(self.data))
		print("hashvalue     : " + str(self.hashvalue))
		return "-----------end--------------"

	#@staticmethod
	def mine_block(self,difficulty=1):
		print("Mining block....")
		mstr=[]
		for i in range(difficulty):
			mstr.append('0')
		j=1
		check=''.join(mstr)
		my_block=block(data=self.data,last_hash=self.last_hash)
		while str(my_block.hashvalue)[0:difficulty]!=check:
			j=j+1
			my_block=block(data=self.data,last_hash=self.last_hash,nounce=j)
		return my_block

	def get_json(self):
		bl={ 'timestamp' : self.timestamp , 'last_hash' : self.last_hash , 'data' : self.data ,'hashvalue' : self.hashvalue }
		return bl

class blockchain():
	bc=[]


	def __init__(self,name,node,port):
		gen_block = block(last_hash="0",data="null")
		self.bc.append(gen_block)

		self.name=name
		self.node=node
		self.port=port

	def __str__ (self):
		print("--B--L--O--C--K--C--H--A--I--N--")
		print("name of chain:"+self.name)
		print("Address :"+ str(self.node) + str(self.port))
		for i in self.bc:
			print(i)
		print("-------E-----N-----D------")
		return ""

	def commit(self,block):
		self.bc.append(block)
		#print("Block successfully append to Blockchain!")

	def get_last_hash(self):
		return self.bc[-1].hashvalue

	def gl(self):
		return len(self.bc)

	def get_json(self):
		my={ 'name' : self.name , 'node': self.node , 'port': self.port, 'blocks' : 'none' }
		bl={}
		for i in range(self.gl()):
			j={ "block-" +str(i) : "blockdata is"+str(i) }
			bl.update(j)
		i=0
		for j in self.bc:
			name="block-"+str(i)
			bl[name]=j.get_json()
			i=i+1
		my['blocks']=bl
		return my
	def empty_bc(self):
		self.bc.clear()
	def reset_with_json_data(self,data):
		self.empty_bc()






#mbc=blockchain(name='j',node="1923168686",port="2158")




#gen_block = block(last_hash="0",data="null")
#mbc=blockchain(name='j',node="1923168686",port="2158")
# for i in range(10):
# 	bb=block(data="block"+str(i),last_hash=mbc.get_last_hash())
# 	mbc.commit(bb.mine_block())

# mbc.get_json()

#bc.append(gen_block)

# for i in range(5):
# 	bc.append(block(data="block"+str(i),last_hash=bc[-1].hashvalue))

# for j in bc:
# 	print(j)

#for i in range(20):
	#j=block.mine_block(data="block".encode()+str(i).encode(),last_hash=bc[-1].hashvalue,difficulty=5)
	#print(j)


#for i in bc:
#	print(i)
