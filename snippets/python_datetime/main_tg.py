import datetime

import pytz


def main():
    zone = pytz.timezone("Asia/Calcutta")
    zone.localize(datetime.datetime(2024, 12, 7, 15, 27, 38, 56789))
    # print(f"%E = {dt:%E}")
    # print(f"%i = {dt:%i}")
    # print(f"%J = {dt:%J}")
    # print(f"%K = {dt:%K}")
    # print(f"%k = {dt:%k}")
    # print(f"%L = {dt:%L}")
    # print(f"%l = {dt:%l}")
    # print(f"%N = {dt:%N}")
    # print(f"%n = {dt:%n}")
    # print(f"%O = {dt:%O}")
    # print(f"%o = {dt:%o}")
    # print(f"%P = {dt:%P}")
    # print(f"%Q = {dt:%Q}")
    # print(f"%q = {dt:%q}")
    # print(f"%s = {dt:%s}")
    # print(f"%v = {dt:%v}")
    # for x in range(26):
    #     cp, sm = chr(65+x), chr(97+x)
    #     print(f"print(f\"%{cp} = {{dt:%{cp}}}\")")
    #     print(f"print(f\"%{sm} = {{dt:%{sm}}}\")")


if __name__ == "__main__":
    main()
