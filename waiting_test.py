import os
import numpy as np

import time
import datetime
import pytz 







def wait_time(now,register_datetime): # return time to wait (in seconds)
    fac = 0.75 # %
    tot = 5 # seconds
    
    time_from_now = (register_datetime-now).days*24*60*60+(register_datetime-now).seconds
    return int(time_from_now*fac)-tot
    
    #time_from_now = (register_datetime-now).days*24*60*60+(register_datetime-now).seconds
    #return int((time_from_now-tot)*fac)


reg_datetime = datetime.datetime.strptime('2019-03-12 14:54','%Y-%m-%d %H:%M')
reg_datetime = pytz.timezone('Europe/Berlin').localize(reg_datetime)

# wait for some % (90%) of wait_time, repeat; aim for some (30) seconds before reg_time
t = wait_time(datetime.datetime.now(pytz.timezone('Europe/Berlin')),reg_datetime)
print('now='+str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+', wait='+str(t)+' until '+str(reg_datetime))
while t > 0: # what happens if registration is already open? -> should work as normal?
    #with open(log_file,'a') as log: # wait for X time until tournament
     #   log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  ')
    time.sleep(t)
    t = wait_time(datetime.datetime.now(pytz.timezone('Europe/Berlin')),reg_datetime)
    print('now='+str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+', wait='+str(t)+' until '+str(reg_datetime))
