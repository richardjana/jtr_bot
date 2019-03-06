import time
import datetime


# Zeitumstellung wie handeln? Helfen da Zeitzonen?
    # https://stackoverflow.com/questions/12203676/daylight-savings-time-in-python

import pytz

# -> datetime.datetime.now(<time_zone>) should always work and be preferred, or work with UTC
# datetime.timedelta() DOES NOT account for daylight saving.
# Do your time add/subtract in UTC timezone ALWAYS. Cast to local time only for output / display.

# now(tz) and utcnow().astimezone(tz) should be equivalent
# tz_list = ['Europe/Berlin','GMT','UTC','UCT','CET']

# naechste Zeitumstellungen:
    # 31.03.2019 02:00 -> 03:00
    # 27.10.2019 03:00 -> 02:00

#real test: time from now until datetime after dst switch (2019-05-03 20:00 Uhr)
# result:
    # wintertime: berlin = utc + 2
    # summertime: berlin = utc + 1

then_naive = datetime.datetime(2019,05,03,20,00,00)
now_naive = datetime.datetime(2019,03,06,17,00,00)
print('naive:  '+str(then_naive)+' - '+str(now_naive)+' = '+str(then_naive-now_naive))
# wrong: 2019-05-03 20:00:00 - 2019-03-06 17:00:00 = 58 days, 3:00:00

then_naive = pytz.timezone('Europe/Berlin').localize(then_naive)
now_naive = pytz.timezone('Europe/Berlin').localize(now_naive)

now_berlin = now_naive.astimezone(pytz.timezone('Europe/Berlin'))
then_berlin = then_naive.astimezone(pytz.timezone('Europe/Berlin'))
print('Berlin: '+str(then_berlin)+' - '+str(now_berlin)+' = '+str(then_berlin-now_berlin))
# right: 2019-05-03 20:00:00+02:00 - 2019-03-06 17:00:00+01:00 = 58 days, 2:00:00

now_utc = now_naive.astimezone(pytz.timezone('UTC'))
then_utc = then_naive.astimezone(pytz.timezone('UTC'))
print('UTC:    '+str(then_utc)+' - '+str(now_utc)+' = '+str(then_utc-now_utc))
# right: 2019-05-03 18:00:00+00:00 - 2019-03-06 16:00:00+00:00 = 58 days, 2:00:00

print('')

# without DST shift
then_naive = datetime.datetime(2019,03,30,20,00,00)
now_naive = datetime.datetime(2019,03,06,17,00,00)
print('naive:  '+str(then_naive)+' - '+str(now_naive)+' = '+str(then_naive-now_naive))
# right: 2019-03-30 20:00:00 - 2019-03-06 17:00:00 = 24 days, 3:00:00

then_naive = pytz.timezone('Europe/Berlin').localize(then_naive)
now_naive = pytz.timezone('Europe/Berlin').localize(now_naive)

now_berlin = now_naive.astimezone(pytz.timezone('Europe/Berlin'))
then_berlin = then_naive.astimezone(pytz.timezone('Europe/Berlin'))
print('Berlin: '+str(then_berlin)+' - '+str(now_berlin)+' = '+str(then_berlin-now_berlin))
# right: 2019-03-30 20:00:00+01:00 - 2019-03-06 17:00:00+01:00 = 24 days, 3:00:00

now_utc = now_naive.astimezone(pytz.timezone('UTC'))
then_utc = then_naive.astimezone(pytz.timezone('UTC'))
print('UTC:    '+str(then_utc)+' - '+str(now_utc)+' = '+str(then_utc-now_utc))
# right: 2019-03-30 19:00:00+00:00 - 2019-03-06 16:00:00+00:00 = 24 days, 3:00:00
