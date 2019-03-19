 # python2 libraries (mechanize)
import os
import numpy as np

import time
import datetime
import pytz

import webbrowser
import mechanize

# save website source to file

def datetime_to_string(dt):
    dt = str(dt)
    return dt[:10]+'_'+dt[11:19]

def scrape_source(url):
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    
    output_file = dir_name+'/ranking_'+datetime_to_string(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+'.html' # get date and time to register
    response = br.open(url)
    with open(output_file,'w') as f:
        f.write(response.read())
        
    return output_file # name of the html source file just written

def wait_noon_midnight():
    t = datetime.datetime.now(pytz.timezone('Europe/Berlin')).time()
    
    return ((11-t.hour%12)*60+(59-t.minute))*60+(60-t.second) # seconds

url = 'https://turniere.jugger.org/rank.team.php'
log_file = 'jtr_ranking_scraper.log'
dir_name = 'ranking_scraper-raw_data'
wait_time = 24*60*60 # 24 hours (in seconds)


### initialize: start log-file; create raw data directory; wait for noon or midnight
with open(log_file,'w') as log:
    log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  starting to scrape ranking table every 12 hours (noon and midnight approx.)\n')

try:
    os.mkdir(dir_name)
except FileExistsError:
    print('Raw data directory already existed. Writing into it.')

time.sleep(wait_noon_midnight())

### keep waiting and downloading
while True:
    output_file = scrape_source(url)
    with open(log_file,'a') as log:
        log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  "'+str(url)+'" downloaded to"'+str(output_file)+'"\n')
    time.sleep(wait_noon_midnight())
