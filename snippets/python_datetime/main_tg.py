import datetime

import pytz


def main():
    zone = pytz.timezone('Asia/Calcutta')
    timestamp = zone.localize(
        datetime.datetime(2024, 12, 7, 15, 27, 38, 56789)
    )
    print(f'%A = {timestamp:%A}')
    print(f'%a = {timestamp:%a}')
    print(f'%B = {timestamp:%B}')
    print(f'%b = {timestamp:%b}')
    print(f'%C = {timestamp:%C}')
    print(f'%c = {timestamp:%c}')
    print(f'%D = {timestamp:%D}')
    print(f'%d = {timestamp:%d}')
    # print(f"%E = {dt:%E}")
    print(f'%e = {timestamp:%e}')
    print(f'%F = {timestamp:%F}')
    print(f'%f = {timestamp:%f}')
    print(f'%G = {timestamp:%G}')
    print(f'%g = {timestamp:%g}')
    print(f'%H = {timestamp:%H}')
    print(f'%h = {timestamp:%h}')
    print(f'%I = {timestamp:%I}')
    # print(f"%i = {dt:%i}")
    # print(f"%J = {dt:%J}")
    print(f'%j = {timestamp:%j}')
    # print(f"%K = {dt:%K}")
    # print(f"%k = {dt:%k}")
    # print(f"%L = {dt:%L}")
    # print(f"%l = {dt:%l}")
    print(f'%M = {timestamp:%M}')
    print(f'%m = {timestamp:%m}')
    # print(f"%N = {dt:%N}")
    # print(f"%n = {dt:%n}")
    # print(f"%O = {dt:%O}")
    # print(f"%o = {dt:%o}")
    # print(f"%P = {dt:%P}")
    print(f'%p = {timestamp:%p}')
    # print(f"%Q = {dt:%Q}")
    # print(f"%q = {dt:%q}")
    print(f'%R = {timestamp:%R}')
    print(f'%r = {timestamp:%r}')
    print(f'%S = {timestamp:%S}')
    # print(f"%s = {dt:%s}")
    print(f'%T = {timestamp:%T}')
    print(f'%t = {timestamp:%t}')
    print(f'%U = {timestamp:%U}')
    print(f'%u = {timestamp:%u}')
    print(f'%V = {timestamp:%V}')
    # print(f"%v = {dt:%v}")
    print(f'%W = {timestamp:%W}')
    print(f'%w = {timestamp:%w}')
    print(f'%X = {timestamp:%X}')
    print(f'%x = {timestamp:%x}')
    print(f'%Y = {timestamp:%Y}')
    print(f'%y = {timestamp:%y}')
    print(f'%Z = {timestamp:%Z}')
    print(f'%z = {timestamp:%z}')
    print(f'in ms = {timestamp.timestamp():0>16.3f}')
    # for x in range(26):
    #     cp, sm = chr(65+x), chr(97+x)
    #     print(f"print(f\"%{cp} = {{dt:%{cp}}}\")")
    #     print(f"print(f\"%{sm} = {{dt:%{sm}}}\")")

    pass


if __name__ == '__main__':
    main()
    pass
