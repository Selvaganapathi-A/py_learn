# Date and time format

## Ghost

| code | example                  | description                                      |
| ---- | ------------------------ | ------------------------------------------------ |
| %a   | Wed                      | day of the week                                  |
| %A   | Wednesday                | day of the week                                  |
| %b   | Jan                      | month                                            |
| %B   | January                  | month                                            |
| %c   | Wed Jan 19 22:23:24 2000 | formatted date                                   |
| %C   | 20                       | century of the year                              |
| %d   | 19                       | simple day                                       |
| %D   | 01/19/00                 | simple date                                      |
| %e   | 19                       | formatted simple day                             |
| %F   | 2000-01-19               | date                                             |
| %g   | 00                       | last two digits of the year                      |
| %G   | 2000                     | year                                             |
| %h   | Jan                      | month                                            |
| %H   | 22                       | hour in 24 hour format                           |
| %I   | 10                       | Hour (12-hour clock) as a decimal number [01,12] |
| %j   | 019                      | day in year                                      |
| %m   | 01                       | month                                            |
| %M   | 23                       | minute                                           |
| %p   | PM                       | AM or PM                                         |
| %r   | 10:23:24 PM              | time                                             |
| %R   | 22:23                    | time 24 hour format                              |
| %S   | 24                       | seconds                                          |
| %T   | 22:23:24                 | time 24 hour format                              |
| %u   | 3                        | day of the week sun - 7, mon - 1                 |
| %U   | 03                       | Week of the year                                 |
| %V   | 03                       | Week of the year                                 |
| %w   | 3                        | day of the week sun - 0, mon - 1                 |
| %W   | 03                       | Week of the year                                 |
| %x   | 01/19/00                 | simple date                                      |
| %X   | 22:23:24                 | time 24 hour format                              |
| %y   | 00                       | last two digits of the year                      |
| %Y   | 2000                     | year                                             |
| %z   | +0530                    | time zone                                        |
| %Z   | India Standard Time      | time zone name                                   |

## Dragon

| Code | Example                 | Description                                                                                                                                                                      |
| ---- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| %a   | Sun                     | Weekday as locale’s abbreviated name.                                                                                                                                            |
| %A   | Sunday                  | Weekday as locale’s full name.                                                                                                                                                   |
| %w   | 0                       | Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.                                                                                                                |
| %d   | 08                      | Day of the month as a zero-padded decimal number.                                                                                                                                |
| %-d  | 8                       | Day of the month as a decimal number. (Platform specific)                                                                                                                        |
| %b   | Sep                     | Month as locale’s abbreviated name.                                                                                                                                              |
| %B   | September               | Month as locale’s full name.                                                                                                                                                     |
| %m   | 09                      | Month as a zero-padded decimal number.                                                                                                                                           |
| %-m  | 9                       | Month as a decimal number. (Platform specific)                                                                                                                                   |
| %y   | 13                      | Year without century as a zero-padded decimal number.                                                                                                                            |
| %Y   | 2013                    | Year with century as a decimal number.                                                                                                                                           |
| %H   | 07                      | Hour (24-hour clock) as a zero-padded decimal number.                                                                                                                            |
| %-H  | 7                       | Hour (24-hour clock) as a decimal number. (Platform specific)                                                                                                                    |
| %I   | 07                      | Hour (12-hour clock) as a zero-padded decimal number.                                                                                                                            |
| %-I  | 7                       | Hour (12-hour clock) as a decimal number. (Platform specific)                                                                                                                    |
| %p   | AM                      | Locale’s equivalent of either AM or PM.                                                                                                                                          |
| %M   | 06                      | Minute as a zero-padded decimal number.                                                                                                                                          |
| %-M  | 6                       | Minute as a decimal number. (Platform specific)                                                                                                                                  |
| %S   | 05                      | Second as a zero-padded decimal number.                                                                                                                                          |
| %-S  | 5                       | Second as a decimal number. (Platform specific)                                                                                                                                  |
| %f   | 000000                  | Microsecond as a decimal number, zero-padded on the left.                                                                                                                        |
| %z   | +0000                   | UTC offset in the form ±HHMM[SS[.ffffff]] (empty string if the object is naive).                                                                                                 |
| %Z   | UTC                     | Time zone name (empty string if the object is naive).                                                                                                                            |
| %j   | 251                     | Day of the year as a zero-padded decimal number.                                                                                                                                 |
| %-j  | 251                     | Day of the year as a decimal number. (Platform specific)                                                                                                                         |
| %U   | 36                      | Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. |
| %W   | 35                      | Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.             |
| %c   | Sun Sep 8 07:06:05 2013 | Locale’s appropriate date and time representation.                                                                                                                               |
| %x   | 09/08/13                | Locale’s appropriate date representation.                                                                                                                                        |
| %X   | 07:06:05                | Locale’s appropriate time representation.                                                                                                                                        |
| %%   | %                       | A literal '%' character.                                                                                                                                                         |

## Rooster

| Code | Example                 | Description                                                                                                                                                                      |
| ---- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| %a   | Sun                     | Weekday as locale’s abbreviated name.                                                                                                                                            |
| %A   | Sunday                  | Weekday as locale’s full name.                                                                                                                                                   |
| %w   | 0                       | Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.                                                                                                                |
| %d   | 08                      | Day of the month as a zero-padded decimal number.                                                                                                                                |
| %-d  | 8                       | Day of the month as a decimal number. (Platform specific)                                                                                                                        |
| %b   | Sep                     | Month as locale’s abbreviated name.                                                                                                                                              |
| %B   | September               | Month as locale’s full name.                                                                                                                                                     |
| %m   | 09                      | Month as a zero-padded decimal number.                                                                                                                                           |
| %-m  | 9                       | Month as a decimal number. (Platform specific)                                                                                                                                   |
| %y   | 13                      | Year without century as a zero-padded decimal number.                                                                                                                            |
| %Y   | 2013                    | Year with century as a decimal number.                                                                                                                                           |
| %H   | 07                      | Hour (24-hour clock) as a zero-padded decimal number.                                                                                                                            |
| %-H  | 7                       | Hour (24-hour clock) as a decimal number. (Platform specific)                                                                                                                    |
| %I   | 07                      | Hour (12-hour clock) as a zero-padded decimal number.                                                                                                                            |
| %-I  | 7                       | Hour (12-hour clock) as a decimal number. (Platform specific)                                                                                                                    |
| %p   | AM                      | Locale’s equivalent of either AM or PM.                                                                                                                                          |
| %M   | 06                      | Minute as a zero-padded decimal number.                                                                                                                                          |
| %-M  | 6                       | Minute as a decimal number. (Platform specific)                                                                                                                                  |
| %S   | 05                      | Second as a zero-padded decimal number.                                                                                                                                          |
| %-S  | 5                       | Second as a decimal number. (Platform specific)                                                                                                                                  |
| %f   | 000000                  | Microsecond as a decimal number, zero-padded on the left.                                                                                                                        |
| %z   | +0000                   | UTC offset in the form ±HHMM[SS[.ffffff]] (empty string if the object is naive).                                                                                                 |
| %Z   | UTC                     | Time zone name (empty string if the object is naive).                                                                                                                            |
| %j   | 251                     | Day of the year as a zero-padded decimal number.                                                                                                                                 |
| %-j  | 251                     | Day of the year as a decimal number. (Platform specific)                                                                                                                         |
| %U   | 36                      | Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. |
| %W   | 35                      | Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.             |
| %c   | Sun Sep 8 07:06:05 2013 | Locale’s appropriate date and time representation.                                                                                                                               |
| %x   | 09/08/13                | Locale’s appropriate date representation.                                                                                                                                        |
| %X   | 07:06:05                | Locale’s appropriate time representation.                                                                                                                                        |
| %%   | %                       | A literal '%' character.                                                                                                                                                         |
