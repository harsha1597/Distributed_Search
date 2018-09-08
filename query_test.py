import pymongo,nltk,string,socket
from nltk.corpus import stopwords,wordnet
client=pymongo.MongoClient('localhost',27017)
db=client.Wordserver
adj=db.adj
noun=db.noun
adv=db.adv
verb=db.verb
tp={'n':noun,'r':adv,'v':verb,'a':adj}
def get_wordnet_pos(tagged):
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
def qsend(q):
    host = socket.gethostname()  
    port = 5000 
    
    self.client_socket = socket.socket()  
    self.client_socket.connect((host, port))
    
    

def query(quer):
    #quer=input("Search :")
    tokens=nltk.word_tokenize(quer)
    tagd=nltk.pos_tag(tokens)
    tagd=get_wordnet_pos(tagd)
    #print(tagd)
    qdict={}
    l=5 # number of clients
    for w in tagd:
        datb=tp[w[1]]
        datb=datb.find({"_id":w[1]},{w[0]:1})
        for x in datb:
            temp=x
            print(temp)
        try:
            temp=temp[w[0]]
            lt=len(temp)
            print(lt,l)
            if(lt<=l):
                qdict[w[0]]=lt
                l=lt
        except:
            pass
        else:
            pass
    print(qdict)
        
    #return tagd
if __name__=="__main__":
    client=pymongo.MongoClient('localhost',27017)
    db=client.Wordserver
    adj=db.adj
    noun=db.noun
    adv=db.adv
    verb=db.verb
    l=5 # count the number of clients
    test=['Most of the adventures recorded in this book really occurred',
          'A Caucus-Race and a Long Tale',
          "Old Muff's Friends--Muff Potter in Court--Muff Potter",
          'The Solemn Oath--Terror Brings Repentance--Mental Punishment']
    for t in test:
        query(t)
    #t=query()
    
    