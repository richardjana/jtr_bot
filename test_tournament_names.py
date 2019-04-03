# python2 libraries (mechanize)

import os
import numpy as np

import time
import datetime
import pytz



def test_mail_subject(subject,tournament_name):
    for i in range(len(subject)-50,5,-1):
        if subject[:i]==subject[-i:]: # is an email with registration link
            if subject[:3]==tournament_name[:3]: # for the correct tournament (HOT FIX)
                return True


def get_register_time_from_jtr(tournament_id):
    t_name = ' '.join(response_words[tn_start:tn_end-10])[7:] # name of the tournament
    
    return t_name


t_names = []


wrong_name = u'12. Th&uuml;ringer Meisterschaft'
right_name = u'12. Th\xfcringer Meisterschaft'


from HTMLParser import HTMLParser
h = HTMLParser()

wrong_name_unescaped = h.unescape(wrong_name)

if right_name==wrong_name_unescaped:
    print(len(right_name))
    print(len(wrong_name_unescaped))
    print(len(wrong_name))
    print('match!')



exit()

print(wrong_name)
print(wrong_name.encode('ascii'))
print(wrong_name.encode('utf-8'))

print(right_name)
#print(right_name.encode('ascii'))
print(right_name.encode('utf-8'))
