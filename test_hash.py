import hashlib,time

for i in range(20):
    j=1
    data="mydata" + str(j) + str(time.time())
    mh=hashlib.sha256(data.encode()).hexdigest()
    print("string is  " + mh )
    
    while str(mh)[0:5]!='00000':
        j+=1
        data="mydata" + str(j) + str(time.time())
        mh=hashlib.sha256(data.encode()).hexdigest()
        #print("--------------->" + str(mh))
    print(mh)
        
        
