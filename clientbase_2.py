#import socket
import nltk,struct,socket,time
from nltk.corpus import stopwords,wordnet
from nltk.stem import WordNetLemmatizer 
from collections import Counter
import string
import json
from os import chdir
import pymongo
#from jsocket import Client
#watchdog with IDLE
     
        #a=aprint("CLient object created Hostname: ",cname,"IP addr: ",ip)


class textfile:
    
      
    defpath=''
    adjsum={}
    nounsum={}
    verbsum={}
    advsum={}
    client=pymongo.MongoClient('localhost',27017)
    #host='localhost'
    #port=8000
    db=client.distsearch
    adj=db.adj
    adj.insert_one({'_id':'a'}) #comment these 4 insert lines while running the 2nd time as you get an error for duplicate id
    noun=db.noun
    noun.insert_one({'_id':'n'})
    adv=db.adv
    adv.insert_one({'_id':'r'})
    verb=db.verb
    verb.insert_one({'_id':'v'})
   
    
    
    def __init__(self):
        #self.defpath=path
        self.ftypes=['n.json','a.json','r.json','v.json']
        #for w in self.ftypes:
        #w=textfile.defpath+'\\'+w
        host = socket.gethostname()  # as both code is running on same pc
        port = 5000  # socket server port number
        
        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((host, port))  # connect to the server           
        self.path=''
        
        #self.name=None
        
        
    def sendname(self,path,files):
        chdir(path)
        for n in files:
            self.word_freq(n)
            
        #self.name=name
        #self.path=textfile.defpath+'\\'+self.name
        
    def getpath(self):
        return self.path+'\\'+self.name
    
    def get_wordnet_pos(self,treebank_tag):

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return 'n'
           
    def client_updatedb(self,path,):
        chdir(path)
        temp=path[-5:]
        
        
        for fpath in self.ftypes:
            rep=''
            f=open(fpath,'r')
            a=(str(json.load(f))+"ACK").encode()
            size=len(a)
            head=struct.pack('cI5s',fpath[0].encode(),size,temp.encode())
        #send details about size and file type
            time.sleep(2)
            while rep!='ACK':
                self.client_socket.send(head)
                time.sleep(2)
                rep=self.client_socket.recv(3).decode()
                if rep=='ACK':
                    self.client_socket.send("ACK".encode())
            rep=''
            
            while rep!='ACK':
                time.sleep(2)
                self.client_socket.send(a)
                time.sleep(2)
                rep=self.client_socket.recv(3).decode()
                #rep='ACK'
                print(rep,"File sent") 
            time.sleep(2) 
            self.client_socket.send('CONT'.encode())  
            print('CONT sent')       
            #print(rep)     
        #time.sleep(2)
        #self.client_socket.send('CLOSE'.encode())
    def closeconn(self):
        self.client_socket.send("CLOS".encode())
        self.client_socket.close()  # close the connection
    
    
    def word_freq(self,name):  #needs to be improved
        """This function returns a FreqDist object which has the frequencies of all the words.The list of words has been filtered for stopwords like 'a' , 'The', etc
        and tokenized"""
        
        lemma=WordNetLemmatizer()
        stop_words=set(stopwords.words("english"))
        stop_words.update(string.punctuation,'A')
        stop_words.add("'s")
        translation = str.maketrans("","", string.punctuation);
        #print(stop_words)
        try:
            
            with open(name, 'r', encoding="utf", errors="backslashreplace") as f: 
                data = f.read()    
        except Exception as e :
            print(str(e))                                                   
                      
        tokens=nltk.word_tokenize(data)
        tagd=nltk.pos_tag(tokens)
        #text=nltk.Text(tokens) 
        filtered=[]
        try:
            for w in tagd:
                if w[0].lower() not in stop_words and w[0]:
                    temp=self.get_wordnet_pos(w[1])
                    new = w[0].translate(translation);
                    temp1=lemma.lemmatize(new.lower(),pos=temp)
                    filtered.append((temp1.lower(),temp))
        except Exception as e:
            print(w[1]) 
            print(str(e))           
                
        fdist=dict(nltk.FreqDist(filtered))
        try:
            
            for k,v in fdist.items():
                if k[1]=='r' and k[0]:
                    self.advsum=dict(Counter(self.advsum)+Counter({k[0]:v}))
                    textfile.adv.update_one({'_id':k[1]},{'$addToSet':{k[0]:{str(v):name}}})
                if k[1]=='a' and k[0]:
                    self.adjsum=dict(Counter(self.adjsum)+Counter({k[0]:v}))
                    textfile.adj.update_one({'_id':k[1]},{'$addToSet':{k[0]:{str(v):name}}})
                if k[1]=='n' and k[0]:
                    self.nounsum=dict(Counter(self.nounsum)+Counter({k[0]:v}))
                    textfile.noun.update_one({'_id':k[1]},{'$addToSet':{k[0]:{str(v):name}}})
                if k[1]=='v' and k[0]:
                    self.verbsum=dict(Counter(self.verbsum)+Counter({k[0]:v}))
                    textfile.verb.update_one({'_id':k[1]},{'$addToSet':{k[0]:{str(v):name}}})
        except Exception as e:
            print(k,v)
            print(str(e))
        for w in ['a','r','n','v']:
            self.dictupdat(w)
            
            
        #print("number of words: ",len(tokens))
        #for w in filtered:
        #    filtered1.append(lemma.lemmatize(w))
        #filteredpos=nltk.pos_tag(filtered1)
        #namedent=nltk.ne_chunk(filteredpos,binary=True)                                                                                   
        #namedent.draw()                                                                           
        #return fdist                                                                        
                    
    def dictupdat(self,typf):
        """THis function adds dictionaries from different files """
        
        w=open(typf+".json","w")
        if typf=='a':
            json.dump(self.adjsum,w)
        if typf=='r':
            json.dump(self.advsum,w)
        if typf=='n':
            json.dump(self.nounsum,w)
        if typf=='v':
            json.dump(self.verbsum,w)
        w.close()
        #sw.close()
        #return  self.senddict
    def getverbsum(self):
        return self.verbsum
        
        
        
    
    
    

    #print(len(x1))
    #a=x.dictupdat({'a':3})
    #a=x.dictupdat({'a':2,'b':3})
