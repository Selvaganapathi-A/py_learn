import datetime
import os
import string


def numberToBase(n: int, b: int) -> list[int]:
    if n == 0:
        return [0]
    digits: list[int] = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


if __name__ == '__main__':
    os.system('clear')
    text = string.digits + string.ascii_uppercase + string.ascii_lowercase + '_-'
    mapped = {x: text[x] for x in range(len(text))}
    reverse_mapped = {text[x]: x for x in range(len(text))}
    # ts: float = 9_168_944_014_211_452.0
    ts: float = datetime.datetime.now().timestamp() * 1_000_000
    number: int = 987
    base = len(text)
    converted = []
    print(mapped)
    print(reverse_mapped)
    print(f'{int(ts):>13n}')
    print(
        ''.join(mapped.get(x, '') for x in numberToBase(int(ts), base)),
    )
    print(
        ''.join(mapped.get(x, '') for x in numberToBase(number, base)),
        base,
    )
    """
168944014211452.0
cQTNz3by
    """
