import socket as so
import nltk as np
from nltk.corpus import stopwords
#from nltk.stem import WordNetLemmatizer 
from collections import Counter
import string
import pickle
#watchdog with IDLE
class clientbase:
    
    
    def __init__(self,cname=so.gethostname(),ip=so.gethostbyname(so.gethostname())):
        self.cname=cname
        self.ip=ip
        self.senddict=np.FreqDist(None)
        #a=aprint("CLient object created Hostname: ",cname,"IP addr: ",ip)
    
    def word_freq(self,f1):  #needs to be improved
        """This function returns a FreqDist object which has the frequencies of all the words.The list of words has been filtered for stopwords like 'a' , 'The', etc
        and tokenized"""
        
        stop_words=set(stopwords.words("english"))
        stop_words.update(string.punctuation,'A')
        stop_words.add("'s")
        #print(stop_words)
        try: 
            f=open(f1)
            with open(f1, 'r', encoding="ascii", errors="surrogateescape") as f:  #surrogateescape for handling non ascii chars in the file
                data = f.read()                                                       
            tokens=np.word_tokenize(data)
            filtered=[w.lower() for w in tokens if not w in stop_words] 
            fdist=np.FreqDist(w.lower() for w in filtered)
            self.dictupdat(fdist)
            return fdist                                                                        
                
        except Exception as e :
            print(str(e))
    
    def dictupdat(self,fdic):
        """THis function adds dictionaries from different files """
        
        #w=csv.writer(open("send_"+self.cname+"_"+self.ip+".csv","w"))  
        w=open("send_"+self.cname+"_"+self.ip+".pkl","wb")
        self.senddict=Counter(self.senddict)+Counter(fdic)
        #w.writerow([key,val] for key,val in self.senddict.items())
        pickle.dump(self.senddict,w)
        w.close()
        #sw.close()
        #return  self.senddict
    def getsenddict(self):
        return self.senddict
        
        
    
    
    
if __name__=="__main__":
    x=clientbase()
    a=x.word_freq("1.txt")
    x1=x.getsenddict()
    print(len(x1))
    x.word_freq("2.txt")
    x1=x.getsenddict()
    print(len(x1))
    x.word_freq("3.txt")
    x1=x.getsenddict()
    print(len(x1))
    x.word_freq("4.txt")
    x1=x.getsenddict()
    print(len(x1))
    x.word_freq("5.txt")
    x1=x.getsenddict()
    print(len(x1))
    x.word_freq("6.txt")
    x1=x.getsenddict()
    print(len(x1))
    x.word_freq("7.txt")
    x1=x.getsenddict()
    print(len(x1))
    #a=x.dictupdat({'a':3})
    #a=x.dictupdat({'a':2,'b':3})
    #print(a)