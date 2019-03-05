# python2 libraries; change the urllib libraries for python3

#import requests
#import urllib
#import urllib2
import webbrowser
import mechanize

import smtplib
import time
import imaplib
import email

def find_captcha():
    infile = open("results.html",'r')
    d = infile.readlines()
    for i in range(len(d)):
        try:
            if d[i].split()[7] == 'name="control"':
                #print(d[i].split()[0]+d[i].split()[1]+d[i].split()[2])
                #captcha_val = solve_captcha(d[i].split()[0],d[i].split()[1],d[i].split()[2])
                return solve_captcha(d[i].split()[0],d[i].split()[1],d[i].split()[2])
        except:
            continue


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
    for i in range(len(d)):
        #try:
        #    if d[i].split()[2] == 'name="control_val"':
        #        print(d[i].split()[3][7:-1])
        #except:
        #    continue
        try:
            if d[i].split()[7] == 'name="control"':
                captcha_value = solve_captcha(d[i].split()[0],d[i].split()[1],d[i].split()[2])
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
    #for i in range(len(d)):
    #    try:
    #        if d[i].split()[2] == 'name="control_val"':
    #            print(d[i].split()[3][7:-1])
    #    except:
    #        continue
    for i in range(len(d)):
        try:
            if d[i].split()[1] == 'class="success">':
                return True
        except:
            continue
        try:
            if d[i].split()[1] == 'class="advice">':
                #print(d[i+2].split()[5:-5]) # for logfile maybe
                return False
        except:
            continue

def TEST_receive_mail_from_gmail(): # this one works!!!
    # note: mails stay in inbox after reading. will have to works with the id, I guess ...
    # 'https://codehandbook.org/how-to-read-email-from-gmail-using-python/'
    
    my_email = 'jtr.python@gmail.com'
    my_pwd = 'strenggeheim'
    smtp_server = 'imap.gmail.com'
    smtp_port = 993
    
    try:
        mail = imaplib.IMAP4_SSL(smtp_server)
        mail.login(my_email,my_pwd)
    except:
        print('mail login failed')
    
    mail.select('inbox') # search mail in inbox
    type,data = mail.search(None,'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    
    for i in range(first_email_id,latest_email_id+1):
            typ, data = mail.fetch(i, '(RFC822)' )
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    #print('From : ' + email_from + '\n') # sent from; should be 'notify@turniere.jugger.org'
                    #print('Subject : ' + email_subject + '\n')
                    #print(msg.get_payload()[0]) # text, signature, stuff (my emails; JTR is string from the beginning)
                    print(extract_link_from_text( str(msg.get_payload()) ))
                    #print(msg['Received']) # time received email (+stuff); send time not accessible
    
    return 0

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
        print('mail login failed')
    
    message_text = 'test message from python'
    subject = 'test mail'
    #date = 
    #msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (my_email,your_email,subject,date,message_text)
    msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (my_email,your_email,subject,message_text)
    
    mail.sendmail(my_email,your_email,msg)
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
    

def click_email_link():

    
    return 0

def get_register_time_from_jtr():
    # maybe integrate with normal registering function?
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
    for i in range(len(d)):
        try:
            if d[i].split()[7] == 'name="control"':
                captcha_value = solve_captcha(d[i].split()[0],d[i].split()[1],d[i].split()[2])
        except:
            continue
        
    
    return register_time

### todo
# run in background, monitor walltime (system / web source)
# have list of tournaments, with team_name, registration time (in file to read regularly?)
# trigger registration event
# check inbox and confirm link (to complete registration) geht eventuell auch ohne, ueber den "key" aus dem link == control_val ?
# maybe have some kind of logfile?

# trigger
# register tournament (verify)
# loop: wait some time, check for mail (verify the correct mail)
# use link

#register data: datetime, tournamentID, teamID, success?
# try to get datetime from jtr website to be sure to have the right one -> same url as register, but: 
#<div class="content">
#    <p>Die Anmeldung zu diesem Turnier ist erst ab dem [ 2019-04-01 10:00 Uhr ] m&ouml;glich.</p> # format = yyyy-mm-dd time

#https://docs.python.org/3/library/datetime.html
import time
import datetime

#d = timedelta(microseconds=1010000)
#print(d.total_seconds())

print(datetime.date.today())
for i in range(10):
    print(datetime.datetime.now())
    time.sleep(1)

exit()



'''
<div class="success">
        <li>Es wurde eine Email mit dem Freigabeschl&uuml;ssel an die angegebene Adresse versendet.</li>
<div class="advice">
        <li>Es muss ein g&uuml;ltiger Wert in das Pr&uuml;ffeld eingegeben werden.</li> # oder andere Hinweise
'''

# <form action="/tournament.signin.php?id=445" method="post" id="signin">

### neues Team
# Teamname:
# Land:
# Stadt waehlen:
# oder neue Stadt:
'''
<p><input type="hidden" name="control_val" value="174a9535b7fd93ceecbe1fc0392fa0f2" /></p> # benoetigt? aendert sich jedes mal
<p><input class="input" type="text" name="team_name" value="" /> Team <span class="label">*</span><br />
    <select class="input" name="co_select">
        <option value="1">Deutschland</option>
    </select> Land <span class="label">***</span><br />
    <select class="input" name="city_select" style="width: 116px;">
        <option value="13">Freiburg</option>
        <option value="114">Karlsruhe</option>
    </select> oder neu:
    <input class="input" type="text" name="team_city" value="" style="width: 120px;" /> Stadt <span class="label">*</span></p>
'''

### bestehendes Team
'''
<p><select class="input" name="team_select">
<option value="624">Deutschland - Freiburg - Flossenhauer</option>
<option value="49">Deutschland - Freiburg - Gossenhauer</option>
<option value="259">Deutschland - Freiburg - Gossenhauer 2</option>
<option value="226">Deutschland - Freiburg - Gossenhauer Veteranen</option>
<option value="52">Deutschland - Freiburg - Gossenhobbiz</option>
<option value="61">Deutschland - Freiburg - Gossenhoschis</option>
<option value="1124">Deutschland - Freiburg - Gossenkinder</option>
<option value="487">Deutschland - Karlsruhe - TackleTiger</option>
</select></p>
'''

### email
### "captcha"
### Anmelden button
'''
<p><input class="input" type="text" name="team_contact" value="" /> Email <span class="label">**</span><br />
    10 + 4 = <input class="input" type="text" name="control" style="width: 25px;" /> # ja, hier steht das catcha als klartext drin
    <input class="input" type="submit" name="signin" value="Anmelden" style="width: 100px;" /></p>
'''
