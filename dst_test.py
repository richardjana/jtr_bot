import time
import datetime


# Zeitumstellung wie handeln? Helfen da Zeitzonen?
    # https://stackoverflow.com/questions/12203676/daylight-savings-time-in-python

# datetime.datetime.now()
# time_left[i] = (reg_datetime[i]-start_time).days*24*60*60+(reg_datetime[i]-start_time).seconds
# datetime.datetime.strptime(date_string+' '+time_string,'%Y-%m-%d %H:%M')

import pytz

# -> datetime.datetime.now(<time_zone>) should always work and be preferred, or work with UTC
# datetime.timedelta() DOES NOT account for daylight saving.
# Do your time add/subtract in UTC timezone ALWAYS. Cast to local time only for output / display.

# now(tz) and utcnow().astimezone(tz) should be equivalent

# naechte Zeitumstellungen:
    # 31.03.2019 02:00 -> 03:00
    # 27.10.2019 03:00 -> 02:00

#real test: time from now until datetime after dst switch (2019-05-03 20:00 Uhr)
    # 2019-05-03 20:00, Berlin == summer time == 
    # 2019-03-06 17:00, Berlin == winter time == 

then_naive = datetime.datetime(2019,05,03,20,00,00)
now_naive = datetime.datetime(2019,03,06,17,00,00)
print('naive:  '+str(then_naive)+' - '+str(now_naive)+' = '+str(then_naive-now_naive))
# wrong: 20:00:00 -17:00:00 = 58 days, 3:00:00

then_naive = pytz.timezone('Europe/Berlin').localize(then_naive)
now_naive = pytz.timezone('Europe/Berlin').localize(now_naive)

now_berlin = now_naive.astimezone(pytz.timezone('Europe/Berlin'))
then_berlin = then_naive.astimezone(pytz.timezone('Europe/Berlin'))
print('Berlin: '+str(then_berlin)+' - '+str(now_berlin)+' = '+str(then_berlin-now_berlin))
# right: 20:00:00+02:00 - 17:00:00+01:00 = 58 days, 2:00:00

now_utc = now_naive.astimezone(pytz.timezone('UTC'))
then_utc = then_naive.astimezone(pytz.timezone('UTC'))
print('UTC:    '+str(then_utc)+' - '+str(now_utc)+' = '+str(then_utc-now_utc))
# right: 18:00:00+00:00 - 16:00:00+00:00 = 58 days, 2:00:00

print('')

# without DST shift
then_naive = datetime.datetime(2019,03,30,20,00,00)
now_naive = datetime.datetime(2019,03,06,17,00,00)
print('naive:  '+str(then_naive)+' - '+str(now_naive)+' = '+str(then_naive-now_naive))
# wrong: 20:00:00 -17:00:00 = 24 days, 3:00:00

then_naive = pytz.timezone('Europe/Berlin').localize(then_naive)
now_naive = pytz.timezone('Europe/Berlin').localize(now_naive)

now_berlin = now_naive.astimezone(pytz.timezone('Europe/Berlin'))
then_berlin = then_naive.astimezone(pytz.timezone('Europe/Berlin'))
print('Berlin: '+str(then_berlin)+' - '+str(now_berlin)+' = '+str(then_berlin-now_berlin))
# right: 20:00:00+01:00 - 17:00:00+01:00 = 24 days, 3:00:00

now_utc = now_naive.astimezone(pytz.timezone('UTC'))
then_utc = then_naive.astimezone(pytz.timezone('UTC'))
print('UTC:    '+str(then_utc)+' - '+str(now_utc)+' = '+str(then_utc-now_utc))
# right: 19:00:00+00:00 - 16:00:00+00:00 = 24 days, 3:00:00

exit()


tz_list = ['Europe/Berlin','GMT','UTC','UCT','CET']
