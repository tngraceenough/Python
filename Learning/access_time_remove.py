# import os module and time module
import time
import os

#move to downloads directory


os.chdir('/tndlebe/Downloads');

#saving list of files and folders in downloads directory in var called lists


files = os.listdir(os.getcwd());

#get present time + number of secs in 30 days


present_time = time.time()
days = 30*24*60*60

# access log
# loop on files var


for file_name in files:

# check if is file or dir


if not os.path.isdir(file_name):
  
  
#get last access time
  
  
access_time = os.stat(file_name).st_atime

#check if file was access in last 30 days

if access_time &lt; (present_time - days):
  
#remove file if not accessed for last 30 days

os.remove(file_name)
print(file_name + 'removed')

