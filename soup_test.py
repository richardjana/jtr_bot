# python2 libraries (mechanize)

import os
import numpy as np

import time
import datetime
import pytz

import webbrowser
import mechanize

import smtplib
import imaplib
import email

from bs4 import BeautifulSoup

def register(tournament_id,team_id,email):
    url = 'https://turniere.jugger.org/tournament.signin.php?id='+str(tournament_id)
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    
    # solve captcha
    response = br.open(url)
    with open('results-register.html','w') as f:
        f.write(response.read())
    
    return 0

    infile = open('results.html','r') # besser machen ohne file input output
    d = infile.readlines()
    infile.close()
    os.remove('results.html')
    for i in range(len(d)):
        #try:
        #    if d[i].split()[2] == 'name="control_val"': # not sure what control_val is used for; maybe put into logfile?
        #        print(d[i].split()[3][7:-1])
        #except:
        #    continue
        try:
            if d[i].split()[7] == 'name="control"':
                captcha_value = solve_captcha(d[i].split()[0],d[i].split()[1],d[i].split()[2])
                break
        except:
            continue
        
    # submit data to form
    br.select_form(nr=0) # the first form, because it has no name
    br['team_select'] = [team_id,]
    br['team_contact'] = email
    br['control'] = str(captcha_value)
    res = br.submit()
    
    # check for success
    with open('results_submit.html','w') as f: # besser machen ohne file input output
        f.write(res.read())
    
    infile = open('results_submit.html','r')
    d = infile.readlines()
    infile.close()
    os.remove('results_submit.html')
    #for i in range(len(d)):
    #    try:
    #        if d[i].split()[2] == 'name="control_val"': # not sure what control_val is used for; maybe put into logfile?
    #            print(d[i].split()[3][7:-1])
    #    except:
    #        continue
    for i in range(len(d)):
        try:
            if d[i].split()[1] == 'class="success">':
                return d[i-1][20:-6] # name of the tournament
        except:
            continue
        try:
            if d[i].split()[1] == 'class="advice">':
                #print(d[i+2].split()[5:-5]) # for logfile maybe
                return False
        except:
            continue

def click_email_link(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    
    # visit link
    response = br.open(url)
    
    # check for success
    with open('results-click_email_link.html','w') as f:
        f.write(response.read())
    
    return 0

    infile = open('results.html','r') # besser machen ohne file input output
    d = infile.readlines()
    infile.close()
    os.remove('results.html')
    for i in range(len(d)):
        try:
            if d[i].split()[1] == 'class="content">':
                color_string = d[i].split()[3][:-3] # failed = #ff6666
                break
        except:
            continue
    
    if color_string == '#ff6666':
        return False
    else:
        return True

def get_register_time_from_jtr(tournament_id):
    # maybe integrate with normal registering function?
    url = 'https://turniere.jugger.org/tournament.signin.php?id='+str(tournament_id)
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    
    # get date and time to register
    response = br.open(url)
    with open('results-get_register_time_from_jtr.html','w') as f:
        f.write(response.read())
    
    return 0

    infile = open('results.html','r') # besser machen ohne file input output
    d = infile.readlines()
    infile.close()
    os.remove('results.html')
    for i in range(len(d)):
        try:
            if d[i].split()[1] == 'class="content">':
                date_string = d[i+1].split()[10]
                time_string = d[i+1].split()[11]
                # turn into datetime type
                return datetime.datetime.strptime(date_string+' '+time_string,'%Y-%m-%d %H:%M')
        except:
            continue
        
    return datetime.datetime.now(pytz.timezone('Europe/Berlin'))-datetime.timedelta(days=1) # registration already open; timedelta might not really work with timezones
    

### get html and save for test purposes
#register(445,27,'jtr.python@gmail.com')
#click_email_link(url)
#get_register_time_from_jtr(496)

'''
with open('results-get_register_time_from_jtr.html')as file:
    soup = BeautifulSoup(file, 'html.parser')

print(soup.find_all('p')[0]) # register datetime
'''
'''
with open('results-register.html')as file:
    soup = BeautifulSoup(file, 'html.parser')
    
print(soup.title) # tournament title
print(soup.find_all('p')[-7]) # captcha; best way I found
'''
'''
with open('results-click_email_link.html')as file:
    soup = BeautifulSoup(file, 'html.parser')

for inst in soup.find_all('div'): # failure advice
    #print(inst['class'])
    if inst['class'] == [u'advice']:
	print(inst)
'''

with open('results-rank_table.html')as file:
    soup = BeautifulSoup(file, 'html.parser')

rigor = soup.find_all('tr')[2]
print(rigor.find_all('td')[0].get_text()) # rank
print(rigor.find_all('td')[2].get_text())
print(rigor.find_all('td')[4].get_text())
print(rigor.find_all('td')[5].get_text())






