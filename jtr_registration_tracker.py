 # python2 libraries (mechanize)
import os
import numpy as np

import time
import datetime
import pytz

import webbrowser
import mechanize
from bs4 import BeautifulSoup

from glob import *
import matplotlib.pyplot as plt

def scrape_datetime_from_filename(filename):
    return pytz.timezone('Europe/Berlin').localize(datetime.datetime.strptime(filename[-24:-5],'%Y-%m-%d_%H:%M:%S'))

def process_registration_html(filename):
    with open(filename) as fp:
        soup = BeautifulSoup(fp,'html.parser')
    
    data = []
    
    try:
        registered_entries = soup.find_all('table')[1].find_all('tr')
        for entry in registered_entries: # position, team name
            position = entry.find_all('td')[0].get_text()[:-1]
            team_name = entry.find_all('td')[1].get_text()
            data.append([position,team_name])
        
    except:
        return data
    
    try:
        waiting_entries = soup.find_all('table')[2].find_all('tr')
        for entry in waiting_entries: # position, team name
            position = entry.find_all('td')[0].get_text()[:-1]
            team_name = entry.find_all('td')[1].get_text()
            data.append([position,team_name])
    except:
        return data
    
    return data

def datetime_to_string(dt):
    dt = str(dt)
    return dt[:10]+'_'+dt[11:19]

def scrape_source(url):
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    
    output_file = dir_name+'/registration_'+datetime_to_string(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+'.html' # get date and time to register
    response = br.open(url)
    with open(output_file,'w') as f:
        f.write(response.read())
        
    return output_file # name of the html source file just written

def get_register_time_from_jtr(tournament_id):
    # here assume that the registration has not opened yet, because all this only makes sense when tracking from the beginning
    url = 'https://turniere.jugger.org/tournament.signin.php?id='+str(tournament_id)
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    
    # get date and time to register
    response = br.open(url)
    response_words = response.read().split()
    
    for i in range(len(response_words)):
        try:
            if response_words[i][:7] == '<title>':
                tn_start = i
        except:
            continue
        try:
            if response_words[i] == 'Ranglisten</title>':
                tn_end = i
                t_name = ' '.join(response_words[tn_start:tn_end-10])[7:] # name of the tournament
                break
        except:
            continue
    for i in range(len(response_words)):
        try:
            if response_words[i] == 'class="content">':
                date_string = response_words[i+11]
                time_string = response_words[i+12]
                return t_name,pytz.timezone('Europe/Berlin').localize(datetime.datetime.strptime(date_string+' '+time_string,'%Y-%m-%d %H:%M')) # turn into datetime type, aware of Berlin tz
        except:
            continue

def wait_time(now,register_datetime): # return time to wait (in seconds)
    fac = 0.5 # %
    tot = 5 # seconds
    
    time_from_now = (register_datetime-now).days*24*60*60+(register_datetime-now).seconds
    
    return int((time_from_now-tot)*fac)

### params
tournamentID = 481 # Jena 2019
url = 'https://turniere.jugger.org/tournament.php?id='+str(tournamentID)
log_file = 'jtr_registration_tracker.log'
dir_name = 'registration_tracker-raw_data-'+str(tournamentID)
sample_wait = 1 # second (is this too close to a DOS attack?)
track_time = 15*60 # 15 minutes

### initialize: start log-file; create raw data directory; wait for start of registration
# get tournament name and start datetime from jtr
tournament_name,register_time = get_register_time_from_jtr(tournamentID)

with open(log_file,'w') as log:
    log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  starting to wait for '+str(tournament_name)+' at '+str(register_time)+'\n')

try:
    os.mkdir(dir_name)
except:
    print('Raw data directory already existed. Writing into it.')

t = wait_time(datetime.datetime.now(pytz.timezone('Europe/Berlin')),register_time)
while t > 0:
    with open(log_file,'a') as log: # wait for X time until tournament
        log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  waiting '+str(t)+' s ('+str(datetime.timedelta(seconds=t))+') for "'+str(tournament_name)+'" at '+str(register_time)+'\n')
    time.sleep(t)
    t = wait_time(datetime.datetime.now(pytz.timezone('Europe/Berlin')),register_time)

### keep downloading every <sample_wait> for <track_time>
for i in range(int(np.ceil(track_time/sample_wait))):
    output_file = scrape_source(url)
    with open(log_file,'a') as log:
        log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  "'+str(url)+'" downloaded to"'+str(output_file)+'"\n')
    time.sleep(sample_wait)

### post-process (plot progress over time)
files_list = glob(dir_name+'/registration_*.html')
times = np.zeros(len(files_list))
n_teams = np.zeros(len(files_list))
for i,filename in enumerate(files_list):
    tdelta = scrape_datetime_from_filename(filename)-register_time
    times[i] = tdelta.seconds+tdelta.microseconds/1000.0 # time after registration opened
    n_teams[i] = len(process_registration_html(filename))

# sort by time
n_teams = n_teams[times.argsort()]
times = times[times.argsort()]

fig,ax = plt.subplots(dpi=100)
ax.semilogx(times,n_teams,'ko-')    
#ax.plot([0,np.max(times)],[capacity,capacity],'k:') # waiting list limit
plt.xlabel('time after registration [s]') # axis scaling should be different I guess
plt.ylabel('number of teams registered')
plt.savefig(dir_name+'/evolution.png')
plt.close()
