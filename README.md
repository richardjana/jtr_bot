# jtr_bot
python script to register for Jugger tournaments automatically

capabilities:
 * check date and time -> trigger for registration
 * fill registration form on jtr website
 * catch email and visit confirmation link

todo:
 * use timezones to catch DST switch
 * forward emails (with updates on tournaments) to another email address
 * log activities

requirements:
 * pytz package for timezones
 * mechanize package, web crawler, needs python2!
   transition to https://github.com/jmcarp/robobrowser instead?
 * time, datetime, pytz, webbrowser, smtplib, imaplib, email (part of python?)
