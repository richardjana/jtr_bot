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
