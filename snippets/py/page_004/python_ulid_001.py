import datetime
import uuid

import pytz
import ulid

if __name__ == '__main__':
    india = pytz.timezone('Asia/Calcutta')
    alaska = pytz.timezone('US/Alaska')
    utc = pytz.timezone('utc')
    india_time = datetime.datetime(2000, 1, 1, 0, 0, 0, 0, india)
    alaska_time = datetime.datetime(2000, 1, 1, 0, 0, 0, 0, alaska)
    utc_time = datetime.datetime(2000, 1, 1, 0, 0, 0, 0, utc)
    print(f'UUID : {uuid.uuid4()}')
    ul: ulid.ULID = ulid.ULID().from_datetime(india_time)
    print(f'ULID : {ul.hex}')
    print(f'ULID : {ul.timestamp}')
    print(f'ULID : {ul.datetime}')
    print(f'ULID : {ul.milliseconds}')
    ul: ulid.ULID = ulid.ULID().from_datetime(alaska_time)
    print(f'ULID : {ul.hex}')
    print(f'ULID : {ul.timestamp}')
    print(f'ULID : {ul.datetime}')
    print(f'ULID : {ul.milliseconds}')
    ul: ulid.ULID = ulid.ULID().from_datetime(utc_time)
    print(f'ULID : {ul.hex}')
    print(f'ULID : {ul.timestamp}')
    print(f'ULID : {ul.datetime}')
    print(f'ULID : {ul.milliseconds}')
    ul2 = ulid.ULID.from_hex(ul.hex)
    print(ul2.datetime)
    print(ul2.hex)
    print(ul.hex)
