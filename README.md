# jtr_bot
python script to register for Jugger tournaments automatically

capabilities:
 * check date and time -> trigger for registration
 * fill registration form on jtr website
 * catch email and visit confirmation link
 * email forwarding by gmail account

todo:
 * make email-address and password global variables, or even better: read from encrypted file somehow
 * quit trying to register after some fixed number of attempts
 * log error message when registration fails
 * periodically do something to show that the script is still running?
 * change waiting parameters (90% -> 75% or even 50%)?
 * send email with attached logfile between sleep() commands?

requirements:
 * pytz package for timezones
 * mechanize package, web crawler, needs python2! (transition to https://github.com/jmcarp/robobrowser instead?)
 * time, datetime, pytz, webbrowser, smtplib, imaplib, email (part of python?)
 
 
 setting up new gmail account:
 * set up new gmail account
 * go to google acoount page -> security -> allow unsecure tech
 * set up forwarding (probably best without filter)

 
 reading tournament table -> logfile:
 * sort by registration datetime
 * add a note what is going to happen with each event
 * maybe some old tournaments get in the way of upcoming ones, ... and then fail repeatedly

 
 encoding special characters in logfile:
 * probably with codecs.open(....,encoding='utf-8') somehow, but did not work on the spot...
