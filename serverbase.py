import socket,json,struct,string
import pymongo,time
import nltk
from nltk.corpus import stopwords,wordnet
#from nltk.stem import WordNetLemmatizer 


class serverbase:
    
    client=pymongo.MongoClient('localhost',27017)
    db=client.Wordserver
    adj=db.adj
    adj.insert_one({'_id':'a'}) #comment these 4 insert lines while running the 2nd time as you get an error for duplicate id
    noun=db.noun
    noun.insert_one({'_id':'n'})
    adv=db.adv
    adv.insert_one({'_id':'r'})
    verb=db.verb
    verb.insert_one({'_id':'v'})
    def __init__(self):
        self.path=None
        self.ndata={}
        self.vdata={}
        self.rdata={}
        self.adata={}
        self.cnames=set()
        host = socket.gethostname()
        port = 5000  
        self.server_socket = socket.socket()  # get instance
            
        self.server_socket.bind((host, port))
    def servermain(self):
        self.server_socket.listen(2)
        conn, address = self.server_socket.accept()  
        print("Connection from: " + str(address))
        self.server_update(conn)
        
        
    
    
    def get_wordnet_pos(self,tagged):
        temp=[]
        stop_words=set(stopwords.words("english"))
        stop_words.update(string.punctuation,'A')
        stop_words.add("'s")
        for w in tagged:
            if w[0] not in stop_words:
                if w[1].startswith('J'):
                    t= wordnet.ADJ
                elif w[1].startswith('V'):
                    t= wordnet.VERB
                elif w[1].startswith('N'):
                        t= wordnet.NOUN
                elif w[1].startswith('R'):
                    t= wordnet.ADV
                else:
                    t= 'n'
                temp.append((w[0],t))
        return temp
    
    def server_update(self,conn):
        rep=''
        
        fset={'a', 'n', 'r', 'v'}
        
        #recieve head packet with details of size and file type
        while rep!='CLOS':
            rep=''
            
            while rep!='ACK':
                data =conn.recv(13)
                print(data)
                h=struct.unpack('cI5s',data)
                ftype=h[0].decode()
                if ftype in fset:
                    time.sleep(2)
                    conn.send("ACK".encode())
                    #print(ftype=='n')
                rep=conn.recv(3).decode()
                print(rep,"Header recieved",ftype)
            rep=''
            #print(ftype=='n')
            #recieve the number of bytes given in previous packet
            while rep!='ACK':
                data=conn.recv(h[1]).decode()
                rep=data[-3:]
                if rep=='ACK':
                    time.sleep(2)
                    conn.send('ACK'.encode())
                    data=data[:-3]
            #f=open(ftype+'serv'+'.json','w')
            #json.dump(data,f)
            #f.close()
            data=data.replace('\'','\"')
                      
            z=json.loads(data)
            print(len(data))
            if ftype=='n':
                self.ndata=z
                print('Donen')
            elif ftype=='a':
                self.adata=z
                print('Donea')
            elif ftype=='r':
                print('Doner')
                self.rdata=z
                
            elif ftype=='v':
                print('Donev')
                self.vdata=z
                
                
            rep=conn.recv(4).decode()       
            print(rep,'End of loop')  
            self.cnames.add(h[2].decode())
            self.dbupdate(h[2].decode(),ftype)
        conn.close()
        print("Socket closed",self.vdata) 
        
        #jdata=json.loads(json.dumps(data))
        #print(type(ndata),address[0]) 
        
    def dbupdate(self,address,ft):
        if ft=='n':
            #print('here',type(self.ndata))
            for k,v in self.ndata.items():
                serverbase.noun.update_one({'_id':'n'},{'$addToSet':{k:{address:str(v)}}})
        elif ft=='a':
            #print('here',len(self.adata))
            for k,v in self.adata.items():
                serverbase.adj.update_one({'_id':'a'},{'$addToSet':{k:{address:str(v)}}})
        elif ft=='r':
            #print('here',len(self.rdata))
            for k,v in self.rdata.items():
                serverbase.adv.update_one({'_id':'r'},{'$addToSet':{k:{address:str(v)}}})
            
        elif ft=='v':
            #print('here',len(self.vdata))
            for k,v in self.vdata.items():
                serverbase.verb.update_one({'_id':'v'},{'$addToSet':{k:{address:str(v)}}})
        
        
    def query(self):
        quer=input("Search :")
        tokens=nltk.word_tokenize(quer)
        tagd=nltk.pos_tag(tokens)
        self.tagd=self.get_wordnet_pos(tagd)
        
        print(self.tagd)
        return self.tagd
        
if __name__=="__main__":
    x=serverbase()
    #x.query()
    x.servermain()
    x.server_update()
    x.dbupdate('Harsha')
    
    
    