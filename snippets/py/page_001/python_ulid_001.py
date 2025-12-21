if __name__ == '__main__':
    import datetime
    import uuid

    import pytz
    import ulid

    utc = pytz.timezone('utc')
    india = pytz.timezone('Asia/Calcutta')
    alaska = pytz.timezone('US/Alaska')
    #
    datetime_ = datetime.datetime(2000, 1, 1, 0, 0, 0, 0)
    #
    utc = utc.localize(datetime_)
    india_time = india.localize(datetime_)
    alaska_time = alaska.localize(datetime_)
    #
    print(f'UUID : {uuid.uuid4()}')
    print()
    #
    ul: ulid.ULID = ulid.ULID().from_datetime(india_time)
    print(f'ULID IN  : {ul.hex}')
    print(f'ULID IN  : {ul.datetime}')
    print(f'ULID IN  : {ul.timestamp}')
    print(f'ULID IN  : {ul.milliseconds}')
    print()
    #
    ul: ulid.ULID = ulid.ULID().from_datetime(alaska_time)
    print(f'ULID ala : {ul.hex}')
    print(f'ULID ala : {ul.datetime}')
    print(f'ULID ala : {ul.timestamp}')
    print(f'ULID ala : {ul.milliseconds}')
    print()
    #
    ul: ulid.ULID = ulid.ULID().from_datetime(utc)
    print(f'ULID utc : {ul.hex}')
    print(f'ULID utc : {ul.datetime}')
    print(f'ULID utc : {ul.timestamp}')
    print(f'ULID utc : {ul.milliseconds}')
    print()
    #
    ul2 = ulid.ULID.from_hex(ul.hex)
    print(ul2.datetime)
    print(ul2.hex)
    print(ul.hex)
