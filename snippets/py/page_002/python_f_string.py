import locale
from datetime import datetime, timedelta, timezone

locale.setlocale(locale.LC_ALL, 'en_in')
arbitrary_number = 1000
print(f'Number      : {arbitrary_number:32}.')
print(f'Binary      : {arbitrary_number:32b}.')
print(f'Octal       : {arbitrary_number:32o}.')
print(f'Hexadecimal : {arbitrary_number:32x}.')
arbitrary_number = 1348293000
print(f'Number      : {arbitrary_number:,.2f}.')
print(f'Number      : {arbitrary_number:_.2f}.')
arbitrary_number = 10002384923
print(f'Number      : {arbitrary_number:32}.')
print(f'Number      : {arbitrary_number:>32}.')
print(f'Number      : {arbitrary_number:<32}.')
print(f'Number      : {arbitrary_number:^32}.')
print(f'Number      : {arbitrary_number:32n}.')
print()
arbitrary_number = 44_000_000_000
print(f'Number      :${arbitrary_number:>-32n}.')
print(f'Number      :${arbitrary_number:+32n}.')
print()
arbitrary_number = -44_000000_000
print(f'Number      : {arbitrary_number:-32n}.')
print(f'Number      : {arbitrary_number:+32n}.')
arbitrary_number = 20937.6503483
print(f'Number      : {arbitrary_number:>.2f}.')
print(f'Number      : {arbitrary_number:_^20.2f}.')
print(f'Number      : {arbitrary_number:7.2}.')
print(f'Number      : {arbitrary_number:20}.')
arbitrary_number = 29872.35269503
print(f'Number      : {arbitrary_number:.2g}.')
print(f'Number      : {arbitrary_number:.5g}.')
print(f'Number      : {arbitrary_number:.8g}.')
print()
arbitrary_number = 72.35269503
print(f'Number      : {arbitrary_number:,.2g}.')
print(f'Number      : {arbitrary_number:_.2g}.')
arbitrary_number = 45829.35269503
print(f'Number      : {arbitrary_number:,.5g}.')
print(f'Number      : {arbitrary_number:_.5g}.')
arbitrary_number = 4589382472.35269503
print(f'Number      : {arbitrary_number:,.8g}.')
print(f'Number      : {arbitrary_number:_.8g}.')
arbitrary_number = 0.35269503
print(f'Number      : {arbitrary_number:%}.')
print(f'Number      : {arbitrary_number:.2%}.')
print()
india_timezone = timezone(timedelta(hours=5, minutes=30), name='Asia/Calcutta')
australia = timezone(timedelta(hours=1, minutes=0), name='Australia')
dt = datetime.now(tz=india_timezone)
print(dt.isoformat())
print(f'{dt:%Y-%m-%dT%H:%M:%S.%f%z}')
print(f'{dt:%Y-%m-%d}')
print(f'{dt:%H:%M:%S}')
print(f'{dt:%F}')
print(f'{dt:%D}')
print(f'{dt:%j}')
print(f'{dt:%B}')
print(f'{dt:%A}')
