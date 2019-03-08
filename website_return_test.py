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

tournament_id = 445
team_id = 3
email = 'jtr.python@gmail.com'

url = 'https://turniere.jugger.org/tournament.signin.php?id='+str(tournament_id)
br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots

# solve captcha
response = br.open(url)
with open('results.html','w') as f:
    f.write(response.read())
    
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
        
