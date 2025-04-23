import time


def findElement(array: list[int], /, target: int):
    if len(array) < 1:
        return None

    array.sort()

    i: int = 0
    j: int = len(array) - 1
    step: int = 0
    while i < j:
        if array[j] == target:
            return j
        elif array[i] == target:
            return i
        elif j - i == 1:
            return
        step += 1
        mid = (i + j) // 2
        if target < array[mid]:
            j = mid
        else:
            i = mid
        print((
            'stet = {:>5d}; nums : {:>5d};  i = {:>5d};  j = {:>5d}; target = {:>5d}'
        ).format(step, j - i, i, j, target),)
        print(array[i], array[j])
        time.sleep(0.5)


def find(start: int, end: int, /, target: int):
    if target < start or end < target:
        return 'Not in this period'
    i: int = start
    j: int = end
    step: int = 0
    while i < j:
        if j == target:
            return j
        elif i == target:
            return i
        step += 1
        mid = (i + j) // 2
        if target < mid:
            j = mid
        else:
            i = mid
        print((
            'stet = {:>5d}; nums : {:>5d};  i = {:>5d};  j = {:>5d}; target = {:>5d}'
        ).format(step, j - i, i, j, target),)
        time.sleep(0.5)


def test_001():
    for x in range(874, 878):
        print(find(0, 1234, target=x))
        print()
        print(find(0, 1133, target=x))
        print()
        print(find(0, 500, target=x))
        print()
        print('-' * 80)


def test_002():
    data = tuple(map(lambda x: (x, x // 2), range(1, 17)))
    print(data)


def test_003():
    import secrets

    data = tuple(range(500))
    # array = [secrets.choice(data) for _ in range(500)]
    # print(array)
    array = [
        1,
        2,
        4,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        14,
        17,
        19,
        24,
        27,
        30,
        31,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        41,
        42,
        44,
        48,
        49,
        51,
        52,
        53,
        55,
        58,
        59,
        60,
        62,
        65,
        66,
        69,
        70,
        72,
        73,
        74,
        75,
        76,
        79,
        80,
        82,
        83,
        84,
        86,
        87,
        91,
        93,
        94,
        95,
        97,
        98,
        100,
        101,
        102,
        104,
        106,
        107,
        109,
        111,
        112,
        113,
        114,
        116,
        117,
        119,
        120,
        121,
        122,
        123,
        127,
        129,
        130,
        131,
        132,
        133,
        134,
        135,
        137,
        139,
        142,
        143,
        144,
        146,
        149,
        152,
        153,
        154,
        155,
        156,
        157,
        158,
        160,
        161,
        162,
        163,
        164,
        165,
        166,
        167,
        169,
        170,
        171,
        172,
        173,
        174,
        175,
        176,
        177,
        178,
        180,
        181,
        182,
        185,
        186,
        189,
        190,
        192,
        193,
        194,
        195,
        196,
        197,
        198,
        200,
        203,
        204,
        205,
        207,
        210,
        214,
        216,
        218,
        219,
        220,
        223,
        226,
        227,
        228,
        231,
        233,
        235,
        237,
        239,
        240,
        242,
        243,
        244,
        246,
        247,
        249,
        251,
        252,
        253,
        254,
        255,
        259,
        261,
        263,
        265,
        267,
        271,
        272,
        273,
        275,
        276,
        277,
        279,
        281,
        282,
        287,
        288,
        290,
        293,
        295,
        296,
        297,
        298,
        299,
        301,
        302,
        303,
        305,
        306,
        307,
        308,
        309,
        312,
        313,
        314,
        316,
        317,
        320,
        321,
        324,
        325,
        326,
        328,
        329,
        331,
        332,
        333,
        335,
        336,
        337,
        338,
        340,
        342,
        343,
        344,
        345,
        346,
        348,
        349,
        351,
        352,
        354,
        355,
        356,
        359,
        364,
        365,
        366,
        367,
        369,
        370,
        371,
        372,
        373,
        375,
        379,
        380,
        382,
        383,
        384,
        386,
        390,
        395,
        397,
        399,
        400,
        401,
        404,
        405,
        407,
        408,
        409,
        411,
        412,
        413,
        414,
        415,
        417,
        418,
        420,
        421,
        423,
        424,
        425,
        426,
        427,
        428,
        429,
        430,
        432,
        433,
        436,
        438,
        439,
        440,
        442,
        444,
        445,
        446,
        447,
        448,
        450,
        452,
        453,
        455,
        456,
        457,
        458,
        459,
        460,
        463,
        466,
        467,
        468,
        469,
        470,
        471,
        473,
        474,
        475,
        476,
        477,
        478,
        479,
        480,
        481,
        482,
        483,
        485,
        487,
        488,
        491,
        492,
        495,
        496,
        497,
        499,
    ]
    print(findElement(array, 97))
    print(findElement(array, 95))
    print(findElement(array, 101))
    print(findElement(array, 68))

    # array = [
    #     2,
    #     3,
    #     9,
    #     10,
    #     13,
    #     15,
    #     16,
    #     17,
    #     20,
    #     21,
    #     26,
    #     28,
    #     30,
    #     33,
    #     34,
    #     36,
    #     37,
    #     45,
    #     50,
    #     52,
    #     58,
    #     59,
    #     63,
    #     64,
    #     70,
    #     72,
    #     79,
    #     81,
    #     82,
    #     83,
    #     87,
    #     88,
    #     92,
    #     99,
    #     100,
    #     102,
    #     108,
    #     112,
    #     122,
    #     123,
    #     126,
    #     129,
    #     132,
    #     143,
    #     145,
    #     160,
    #     162,
    #     165,
    #     167,
    #     174,
    #     176,
    #     178,
    #     181,
    #     185,
    #     188,
    #     189,
    #     190,
    #     194,
    # ]
    # array = [
    #     8,
    #     10,
    #     16,
    #     20,
    #     23,
    #     24,
    #     26,
    #     33,
    #     35,
    #     36,
    #     37,
    #     42,
    #     45,
    #     49,
    #     62,
    #     65,
    #     68,
    #     73,
    #     82,
    #     92,
    #     93,
    #     94,
    #     95,
    #     99,
    #     101,
    #     104,
    #     105,
    #     106,
    #     114,
    #     116,
    #     118,
    #     123,
    #     125,
    #     128,
    #     131,
    #     135,
    #     139,
    #     140,
    #     153,
    #     154,
    #     156,
    #     159,
    #     160,
    #     165,
    #     167,
    #     169,
    #     172,
    #     181,
    #     188,
    #     192,
    #     196,
    # ]

    # print(sorted(set(array)))
    # array = [secrets.choice(data) for _ in range(64)]
    # print(sorted(set(array)))

    # array = [secrets.choice(data) for _ in range(64)]
    # print(sorted(set(array)))
    # pass


def testcase(condition: int):
    if condition == 1:
        test_001()
    elif condition == 2:
        test_002()
    elif condition == 3:
        test_003()


def main():
    testcase(3)


if __name__ == '__main__':
    import os

    os.system('cls')
    main()
    pass
