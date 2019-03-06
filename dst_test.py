import time
import datetime


# Zeitumstellung wie handeln? Helfen da Zeitzonen?
    # https://stackoverflow.com/questions/12203676/daylight-savings-time-in-python

# datetime.datetime.now()

# time_left[i] = (reg_datetime[i]-start_time).days*24*60*60+(reg_datetime[i]-start_time).seconds

# datetime.datetime.strptime(date_string+' '+time_string,'%Y-%m-%d %H:%M')


import pytz
la = pytz.timezone("America/Los_Angeles")
now = datetime.datetime.now(la) # correct
now2 = la.localize(datetime.datetime.now()) # my local time?

print(now)
print(now2)

utc = pytz.timezone('UTC')
now = utc.localize(datetime.datetime.utcnow())
la = pytz.timezone('America/Los_Angeles')
print(now.astimezone(la)) # also correct

print('')

print(datetime.datetime.utcnow())
utc = pytz.timezone('UTC')
print(utc.localize(datetime.datetime.utcnow()))
print(utc.localize(datetime.datetime.now())) # 1 hour shifted to above line -> winter time?


# -> datetime.datetime.now(<time_zone>) should always work and be preferred, or work with UTC
# datetime.timedelta() DOES NOT account for daylight saving.
# Do your time add/subtract in UTC timezone ALWAYS. Cast to local time only for output / display.

# now(tz) and utcnow().astimezone(tz) should be equivalent


# naechte Zeitumstellungen:
    # 31.03.2019 02:00 -> 03:00
    # 27.10.2019 03:00 -> 02:00
