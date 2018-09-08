import os
import win32file
import win32event
import win32con
import clientbase_2

class clientapp:
    def __init__(self):
        self.path=[]
        #self.path.append(path)
        self.x=clientbase_2.textfile()
        
    def addpath(self,path): 
        self.path.append(path)
        
        
        
    def main(self):
        change_handle={}
        old_path_contents={}
        new_path_contents={}
        for p in self.path:
            temp=win32file.FindFirstChangeNotification(p,0,win32con.FILE_NOTIFY_CHANGE_FILE_NAME)
            change_handle[p]=temp
        try:
            for p in self.path: #To allow multiple directories in a client
                temp=list(p+'\\'+f for f in os.listdir(p) if f[-3:]=='txt')
                old_path_contents[p]=temp
            for p in self.path:
                self.x.client_updatedb(p)
            self.x.closeconn()
            return
           # for k,v in old_path_contents.items():
           #     self.x.sendname(path=k,files=v) #change directory with path
            #x.client_updatedb()
            print('Entering infintite loop')
            while 1:
                for p in self.path:
                    result = win32event.WaitForSingleObject (change_handle[p], 500)
                    if result == win32con.WAIT_OBJECT_0 :
                        break
    
        
                if result == win32con.WAIT_OBJECT_0 : #the constant is 0
                    new_path_contents[p] = list(f for f in os.listdir (p) if f[-3:]=='txt')
                if new_path_contents[p]==old_path_contents[p]:
                    continue
                added = [f for f in new_path_contents[p] if not f in old_path_contents[p]]
                
                self.x.sendname(path=p,files=added)
                print('New json file made')
                deleted = [f for f in old_path_contents[p] if not f in new_path_contents[p]]
                old_path_contents[p] = new_path_contents[p]
                win32file.FindNextChangeNotification (change_handle[p])
                #x.client_updatedb()
    
        finally:
            win32file.FindCloseChangeNotification (change_handle[p])
if __name__=="__main__":
    test=clientapp()
    test.addpath('C:\\Users\\Ramesh\\Documents\\Python Scripts\\Text1')
    test.addpath('C:\\Users\\Ramesh\\Documents\\Python Scripts\\Text2')
    test.addpath('C:\\Users\\Ramesh\\Documents\\Python Scripts\\Text3')
    test.addpath('C:\\Users\\Ramesh\\Documents\\Python Scripts\\Text4')
    test.addpath('C:\\Users\\Ramesh\\Documents\\Python Scripts\\Text5')
    test.main()
    