# python2 libraries (mechanize)

import os
import numpy as np

import time
import datetime
import pytz

import webbrowser
import mechanize

import smtplib
import time
import imaplib
import email

def solve_captcha(i,op,j):
    if op=='+':
        return int(i)+int(j)
    if op=='-':
        return int(i)-int(j)

def register(tournament_id,team_id,email):
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
        print('mail login failed') # should never happen
    
    mail.select('inbox') # search mail in inbox
    type,data = mail.search(None,'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    
    for i in range(latest_email_id+1,first_email_id,-1):
            typ, data = mail.fetch(i,'(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    if msg['subject'][:len(tournament_name)+1]==tournament_name: # mail to the correct tournament
                        url = extract_link_from_text(str(msg.get_payload()))
                        return click_email_link(url) # True if success, False if not

    return False # email with link not found

def check_for_info_mail(last_check_datetime):
    my_email = 'jtr.python@gmail.com'
    my_pwd = 'strenggeheim'
    smtp_server = 'imap.gmail.com'
    smtp_port = 993
    
    try:
        mail = imaplib.IMAP4_SSL(smtp_server)
        mail.login(my_email,my_pwd)
    except:
        print('mail login failed') # should never happen
    
    mail.select('inbox') # search mail in inbox
    type,data = mail.search(None,'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    
    msg_list = []
    target_string = 'JTR | Jugger - Turniere - Ranglisten - '
    for i in range(latest_email_id+1,first_email_id,-1):
            typ, data = mail.fetch(i,'(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    if msg['subject'][:len(target_string)+1]==target_string: # info mail
                        if msg['received']>=<:
                            msg_list.append(msg)

    return msg_list # empty if no new info mails

def forward_mail(msg_list):
    your_email = 'onkel.hotte@gmail.com'
    my_email = 'jtr.python@gmail.com'
    my_pwd = 'strenggeheim'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    
    try:
        mail = smtplib.SMTP_SSL(smtp_server,smtp_port)
        mail.login(my_email,my_pwd)
    except:
        print('mail login failed') # should never happen
    
    for msg in msg_list:
        #rewrite message (necessary?), send
        fwd_msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (my_email,your_email,msg['subject'],str(msg.get_payload()))
        mail.sendmail(my_email,your_email,fwd_msg)
    mail.quit()
    
    return 0

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
    with open('results.html','w') as f:
        f.write(response.read())
    
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
    with open('results.html','w') as f:
        f.write(response.read())
    
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
    
def read_tournament_table(filename):
    infile = open(filename,'r') # besser machen ohne file input output
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
    fac = 0.9
    tot = 30
    
    time_from_now = (register_datetime-now).days*24*60*60+(register_datetime-now).seconds
    
    return int(time_from_now*fac)-tot

#https://docs.python.org/3/library/datetime.html

### starting routine of bot
start_time = datetime.datetime.now(pytz.timezone('Europe/Berlin')) # get current time
log_file = 'jtr_bot.log'

tournamentID,teamID,date_estimate,time_estimate,comment = read_tournament_table('/home/richard/Documents/jtr_bot/tournament_data.txt') # read registration list

reg_datetime = [] # figure out registration times from jtr
time_left = np.zeros(len(tournamentID)) # in seconds (should be good enough)
for i in range(len(tournamentID)):
    reg_datetime.append(get_register_time_from_jtr(tournamentID[i]))
    time_left[i] = (reg_datetime[i]-start_time).days*24*60*60+(reg_datetime[i]-start_time).seconds

tournamentID = tournamentID[time_left>0] # remove events from the past
teamID = teamID[time_left>0]
time_left = time_left[time_left>0]

t_order = time_left.argsort() # sort for most urgent events

# start waiting with checks for time, forwarding emails
for i in range(len(tournamentID)): # for loop over future tournaments from list
    # wait for some % (90%) of wait_time, repeat; aim for some (30) seconds before reg_time
    t = wait_time(datetime.datetime.now(pytz.timezone('Europe/Berlin')),reg_datetime[t_order[i]])
    while t > 0: # what happens if registration is already open? -> should work as normal?
        time.sleep(t)
        t = wait_time(datetime.datetime.now(pytz.timezone('Europe/Berlin')),reg_datetime[t_order[i]])
    
    # start trying to register every second (or so); verify
    tournament_name = register(tournament_id,team_id,email)
    while tournament_name==False:
        time.sleep(1)
        tournament_name = register(tournament_id,team_id,email)
    
    # loop: wait some time, check for mail (verify the correct mail with tournament name), use the link
    confirm_link = get_link_from_gmail(tournament_name)
    while confirm_link==False:
        time.sleep(1)
        confirm_link = get_link_from_gmail(tournament_name)
    
    


### open questions
# Zeitumstellung wie handeln? Helfen da Zeitzonen? -> datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    # wie eigenen Ort / eigene Zeitzone herausfinden (bis dahin erstmal Berlin verwenden)
# Wie umgehen mit mehreren Teams auf einem Turnier? Passt das von alleine schon ganz gut? (denke ja)
# An welcher Stelle email forwarding einbauen?

### logfile fehlt noch (also email periodically?)




### teamIDs
'''
<option value="624">Deutschland - Freiburg - Flossenhauer
<option value="49">Deutschland - Freiburg - Gossenhauer
<option value="259">Deutschland - Freiburg - Gossenhauer 2
<option value="1124">Deutschland - Freiburg - Gossenkinder
<option value="487">Deutschland - Karlsruhe - TackleTiger
'''
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
