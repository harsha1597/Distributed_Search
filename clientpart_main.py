import os
import win32file
import win32event
import win32con
import clientbase

x=clientbase.clientbase()
path=os.path.abspath('C:\\Users\\Ramesh\\Documents\\Python Scripts\\Text1')
change_handle=win32file.FindFirstChangeNotification(path,0,win32con.FILE_NOTIFY_CHANGE_FILE_NAME)
try:

  old_path_contents = list(f for f in os.listdir (path) if f[-3:]=='txt')
  for w in old_path_contents:
      x.word_freq(w)
  while 1:
    result = win32event.WaitForSingleObject (change_handle, 500)

    #
    # If the WaitFor... returned because of a notification (as
    #  opposed to timing out or some error) then look for the
    #  changes in the directory contents.
    #
    if result == win32con.WAIT_OBJECT_0 :
      new_path_contents = list(f for f in os.listdir (path) if f[-3:]=='txt')
      if new_path_contents==old_path_contents:
          continue
      added = [f for f in new_path_contents if not f in old_path_contents]
      x.word_freq(w for w in added)
      print('New pickle file made')
      deleted = [f for f in old_path_contents if not f in new_path_contents]
      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification (change_handle)

finally:
  win32file.FindCloseChangeNotification (change_handle)