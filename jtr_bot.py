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

def solve_captcha(i,op,j):
    if op=='+':
        return int(i)+int(j)
    if op=='-':
        return int(i)-int(j)

def register(tournament_id,team_id,my_email):
    url = 'https://turniere.jugger.org/tournament.signin.php?id='+str(tournament_id)
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    
    # solve captcha
    response = br.open(url)
    response_words = response.read().split()

    for i in range(len(response_words)):
        #try:
        #    if response_words[i] == 'name="control_val"': # not sure what control_val is used for; maybe put into logfile?
                #with open('jtr_bot.log','a') as log:
                 #   log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  registration page control_val = '+str(response_words[i+1][7:-1])+'\n')
        #except:
        #    continue
        try:
            if response_words[i] == 'name="control"':
                captcha_value = solve_captcha(response_words[i-7],response_words[i-6],response_words[i-5])
                break
        except:
            continue
    
    try:
        # submit data to form
        br.select_form(nr=0) # the first form, because it has no name
        br['team_select'] = [str(team_id),]
        br['team_contact'] = my_email
        br['team_repeat'] = my_email
        br['control'] = str(captcha_value)
        response = br.submit()
    except: # catch if registration not open yet
        with open('jtr_bot.log','a') as log:
            log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  registration not open yet\n')
        return False
    
    # check for success
    response_words = response.read().split()

    #for i in range(len(d)):
    #    try:
    #        if response_words[i] == 'name="control_val"': # not sure what control_val is used for; maybe put into logfile?
                #with open('jtr_bot.log','a') as log:
                 #   log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  registration return page control_val = '+str(response_words[i+1][7:-1])+'\n')
    #    except:
    #        continue
    for i in range(len(response_words)):
        try:
            if response_words[i] == 'class="success">':
                return True # name of the tournament not necessary anymore, because this now comes from get_register_time_from_jtr
                    
        except:
            continue
        try:
            if response_words[i] == 'class="advice">':
                #print(d[i+2].split()[5:-5]) # for logfile maybe
                #with open('jtr_bot.log','a') as log:
                 #   log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  ')
                return False
        except:
            continue

def get_link_from_gmail(tournament_name):
    # note: mails stay in inbox after reading. will have to works with the id, I guess ...
    # 'https://codehandbook.org/how-to-read-email-from-gmail-using-python/'
    
    ### email types freom jtr ('notify@turniere.jugger.org'):
    # msg['subject']
    # registration link: '<t_name> - Team anmelden - JTR | Jugger - Turniere - Ranglisten - <t_name>'
    # registration confirmation: 'JTR | Jugger - Turniere - Ranglisten'
    # update on tournament: 'JTR | Jugger - Turniere - Ranglisten - <t_name>'
        
    # msg['from'] # should be 'notify@turniere.jugger.org'
    # msg['Received'] # time received email (+stuff); send time not accessible
    # msg.get_payload()[0] # text, signature, stuff (my emails; JTR is string from the beginning)
    
    my_email = 'jtr.python@gmail.com'
    my_pwd = 'strenggeheim'
    smtp_server = 'imap.gmail.com'
    smtp_port = 993
    
    try:
        mail = imaplib.IMAP4_SSL(smtp_server)
        mail.login(my_email,my_pwd)
    except:
        with open('jtr_bot.log','a') as log: # should never happen
            log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  login to imap server failed in get_link_from_gmail\n')
    
    mail.select('inbox') # search mail in inbox
    type,data = mail.search(None,'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    
    for i in range(latest_email_id,first_email_id-1,-1):
            typ, data = mail.fetch(i,'(RFC822)')
            if isinstance(data[0][1], tuple):
                msg = email.message_from_string(data[0][1])
                if msg['subject'][:len(tournament_name)+1]==tournament_name: # mail to the correct tournament
                    url = extract_link_from_text(str(msg.get_payload()))
                    return click_email_link(url) # True if success, False if not

    return False # email with link not found

def extract_link_from_text(message_text):
    target_string = 'http://turniere.jugger.org/activate.php'
    try:
        for i in range(len(message_text)):
            if message_text[i:i+len(target_string)] == target_string:
                return message_text[i:i+85] # length of link
    except:
        pass
    
    return ''

def click_email_link(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    
    # visit link
    response = br.open(url)
    
    # check for success
    response_words = response.read().split()

    for i in range(len(response_words)):
        try:
            if response_words[i] == 'style="background-color:':
                color_string = response_words[i+1][:7] # failed = #ff6666, success = #99ff99
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
    
    return t_name,datetime.datetime.now(pytz.timezone('Europe/Berlin'))-datetime.timedelta(days=1) # registration already open; timedelta might not really work with timezones
    
def read_tournament_table(filename):
    infile = open(filename,'r')
    lines = infile.readlines()
    infile.close()
    
    #TournamentID TeamID registered registration_date(estimate) registration_date(estimate) comment
    tournamentID = np.zeros(len(lines)-1,dtype=np.int16)
    teamID = np.zeros(len(lines)-1,dtype=np.int16)
    date_estimate = []
    time_estimate = []
    comment = []
    
    for i,line in enumerate(lines):
        if i==0: # remove column header
            continue
        
        tournamentID[i-1] = line.split()[0]
        teamID[i-1] = line.split()[1]
        date_estimate.append(line.split()[2])
        time_estimate.append(line.split()[3])
        comment.append(line.split()[4])
    
    return tournamentID,teamID,date_estimate,time_estimate,comment
    
def wait_time(now,register_datetime): # return time to wait (in seconds)
    fac = 0.9 # %
    tot = 30 # seconds
    
    time_from_now = (register_datetime-now).days*24*60*60+(register_datetime-now).seconds
    
    return int((time_from_now-tot)*fac)


### dict with teamIDs : team names
team_names = {  '49':'Gossenhauer',
               '259':'Gossenhauer 2',
               '487':'TackleTiger',
               '624':'Flossenhauer',
              '1124':'Gossenkinder'}

### starting routine of bot
start_time = datetime.datetime.now(pytz.timezone('Europe/Berlin')) # get current time
#log_file = 'jtr_bot.log'
my_email = 'jtr.python@gmail.com'
attempt_sleep_time = 1 # seconds between attempts to jtr website / gmail

tournamentID,teamID,date_estimate,time_estimate,comment = read_tournament_table('./tournament_data.txt') # read registration list

reg_datetime = [] # figure out registration times from jtr
tournament_name = [] # also get name of tournament as string
time_left = np.zeros(len(tournamentID)) # in seconds (should be good enough)
for i in range(len(tournamentID)):
    tn, reg_time = get_register_time_from_jtr(tournamentID[i])
    reg_datetime.append(reg_time)
    tournament_name.append(tn)
    time_left[i] = (reg_datetime[i]-start_time).days*24*60*60+(reg_datetime[i]-start_time).seconds

tournamentID = tournamentID[time_left>0] # remove events from the past
teamID = teamID[time_left>0]
time_left = time_left[time_left>0]

t_order = time_left.argsort() # sort for most urgent events

with open('jtr_bot.log','w') as log: # initialization; list of tournaments to register for; also test email servers (don't actually send?)
    log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  initializing jtr_bot.py\n')
    for i in range(len(tournamentID)): # reg_time, tournament, team
        log.write('    '+str(reg_datetime[t_order[i]])+', '+str(tournament_name[t_order[i]])+', '+str(team_names[str(teamID[t_order[i]])])+'\n')

# start waiting with checks for time, forwarding emails
for i in range(len(tournamentID)): # for loop over future tournaments from list
    # wait for some % (90%) of wait_time, repeat; aim for some (30) seconds before reg_time
    t = wait_time(datetime.datetime.now(pytz.timezone('Europe/Berlin')),reg_datetime[t_order[i]])
    while t > 0: # what happens if registration is already open? -> should work as normal?
        with open('jtr_bot.log','a') as log: # wait for X time until tournament
            log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  waiting '+str(t)+' s ('+str(datetime.timedelta(seconds=t))+') for "'+str(tournament_name[t_order[i]])+'" at '+str(reg_datetime[t_order[i]])+'\n')
        time.sleep(t)
        t = wait_time(datetime.datetime.now(pytz.timezone('Europe/Berlin')),reg_datetime[t_order[i]])
    
    # start trying to register every second (or so); verify
    register_success = register(tournamentID[t_order[i]],teamID[t_order[i]],my_email)
    while register_success==False:
        # if JTR registration failed, log is updated there
        time.sleep(attempt_sleep_time)
        register_success = register(tournamentID[t_order[i]],teamID[t_order[i]],my_email)
    with open('jtr_bot.log','a') as log: # JTR registration success
        log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  registration for "'+str(tournament_name[t_order[i]])+'" with team "'+str(team_names[str(teamID[t_order[i]])])+'" successful\n')
    
    # loop: wait some time, check for mail (verify the correct mail with tournament name), use the link
    confirm_link = get_link_from_gmail(tournament_name[t_order[i]])
    while confirm_link==False:
        with open('jtr_bot.log','a') as log: # email confirmation failed
            log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  confirmation for "'+str(tournament_name[t_order[i]])+'" with team "'+str(team_names[str(teamID[t_order[i]])])+'" failed\n')
        time.sleep(attempt_sleep_time)
        confirm_link = get_link_from_gmail(tournament_name[t_order[i]])
    with open('jtr_bot.log','a') as log: # email confirmation success
        log.write(str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))+' :  confirmation for "'+str(tournament_name[t_order[i]])+'" with team "'+str(team_names[str(teamID[t_order[i]])])+'" successful\n')
    


### open questions
# Wie umgehen mit mehreren Teams auf einem Turnier? Passt das von alleine schon ganz gut? (denke ja)

### also email logfile periodically?
### maximum number of failed attempts to jtr / gmail before stopping? -> for loop instead of while?

'''
def send_mail_with_gmail():
    #https://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp
    #https://docs.python.org/3/library/email.utils.html#email.utils.formatdate
    
    your_email = 'jtr.python@gmail.com'
    my_email = 'jtr.python@gmail.com'
    my_pwd = 'strenggeheim'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    
    try:
        mail = smtplib.SMTP_SSL(smtp_server,smtp_port)
        mail.login(my_email,my_pwd)
    except:
        print('mail login failed') # should never happen
    
    message_text = 'test message from python'
    subject = 'test mail'
    #date = 
    #msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (my_email,your_email,subject,date,message_text)
    msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (my_email,your_email,subject,message_text)
    
    mail.sendmail(my_email,your_email,msg)
    mail.quit()
    
    return 0
'''
