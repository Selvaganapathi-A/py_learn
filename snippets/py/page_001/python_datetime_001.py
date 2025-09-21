import datetime
import time

import pytz

"""
| %a | Wed |                        day of the week ||
|%A | Wednesday                  |   day of the week|
|%b | Jan                        |   month|
|%B | January                    |   month|
|%c | Wed Jan 19 22:23:24 2000   |   formatted date|
|%C | 20                         |   century of the year|
|%d | 19                         |   simple day|
|%D | 01/19/00                   |   simple date|
|%e | 19                         |   formatted simple day|
|%F | 2000-01-19                 |   date|
|%g | 00                         |   last two digits of the year|
|%G | 2000                       |   year|
|%h | Jan                        |   month|
|%H | 22                         |   hour in 24 hour format|
|%I | 10                         |   Hour (12-hour clock) as a decimal number [01,12]|
|%j | 019                        |   day in year|
|%m | 01                         |   month|
|%M | 23                         |   minute|
|%p | PM                         |   AM or PM|
|%r | 10:23:24 PM                |   time|
|%R | 22:23                      |   time 24 hour format|
|%S | 24                         |   seconds|
|%T | 22:23:24                   |   time 24 hour format|
|%u | 3                          |   day of the week sun - 7, mon - 1|
|%U | 03                         |   Week of the year|
|%V | 03                         |   Week of the year|
|%w | 3                          |   day of the week sun - 0, mon - 1|
|%W | 03                         |   Week of the year|
|%x | 01/19/00                   |   simple date|
|%X | 22:23:24                   |   time 24 hour format|
|%y | 00                         |   last two digits of the year|
|%Y | 2000                       |   year|
|%z | +0530                      |   time zone|
|%Z | India Standard Time        |   time zone name|
"""
if __name__ == '__main__':
    # unix timestamp
    print(time.time())
    # precision from jan-01, 1970
    print(time.time_ns())
    print(2**31)
    print(2**63)
    india = pytz.timezone('Asia/Kolkata')
    utc = pytz.timezone('UTC')
    date = datetime.datetime.fromtimestamp(2**31 - 1, india)
    print('32-bit max time :-', date)
    print('32-bit max time :-', date.astimezone(utc))
    # pprint.pprint(all_timezones)
    # pprint.pprint(common_timezones)
    some_date = datetime.datetime.fromisoformat('2022-02-05T19:40:00')
    utc = pytz.timezone('UTC')
    india = pytz.timezone('Asia/Kolkata')
    alaska = pytz.timezone('US/Alaska')
    seattle = pytz.timezone('America/Los_Angeles')
    sydney = pytz.timezone('Australia/Sydney')
    print()
    print()
    print('              ', some_date)
    print('Universal Time', utc.localize(some_date))
    print('Alask     Time', alaska.localize(some_date))
    print('India     Time', india.localize(some_date))
    print('Seattle   Time', seattle.localize(some_date))
    print('Sydney    Time', sydney.localize(some_date))
    print()
    india_datetime = india.localize(some_date)
    print('time in India   :', india_datetime)
    print('time in Alaska  :', india_datetime.astimezone(alaska))
    print('time in Seattle :', india_datetime.astimezone(seattle))
    print('time in Sydney  :', india_datetime.astimezone(sydney))
    print('time in UTC     :', india_datetime.astimezone(utc))
    print()
    print('Travel in Flight...')
    print()
    alaska_datetime = alaska.localize(some_date)
    sydney_datetime = sydney.localize(some_date)
    print('Depart in india    :', india_datetime)
    print(
        'Arrive Sydney Time :',
        (india_datetime + datetime.timedelta(hours=21)).astimezone(sydney),
    )
    print()
    print('Depart in India   :', india_datetime)
    print(
        'Arrive in Alaska  :',
        (india_datetime + datetime.timedelta(hours=31, minutes=40)).astimezone(alaska),
    )
    print()
