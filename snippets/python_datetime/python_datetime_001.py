import datetime

import pytz

"""
|%a | Wed                        |   day of the week|
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
if __name__ == "__main__":
    regions: tuple[str, ...] = (
        "UTC",
        "Asia/Kolkata",
        "US/Alaska",
        "America/Los_Angeles",
        "Australia/Sydney",
    )
    # unix timestamp
    # precision from jan-01, 1970
    # print(2**31)
    # print(2**63)
    india = pytz.timezone("Asia/Kolkata")
    utc = pytz.timezone("UTC")
    date = datetime.datetime.fromtimestamp(2**31 - 1, india)
    # pprint.pprint(all_timezones)
    # pprint.pprint(common_timezones)
    some_date = datetime.datetime.fromisoformat("2022-02-05T19:40:00")
    utc = pytz.timezone("UTC")
    india = pytz.timezone("Asia/Kolkata")
    alaska = pytz.timezone("US/Alaska")
    los_angeles = pytz.timezone("America/Los_Angeles")
    sydney = pytz.timezone("Australia/Sydney")

    india_datetime = india.localize(some_date)
    alaska_datetime = alaska.localize(some_date)
    sydney_datetime = sydney.localize(some_date)
