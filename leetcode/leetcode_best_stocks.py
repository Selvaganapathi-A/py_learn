from icecream import ic


def main():
    stock_trace: tuple[float, ...] = (
        125.05,
        124.35,
        118.65,
        123.4,
        127.9,
        125.9,
        124.7,
        123.85,
        125.05,
        125.1,
        124.25,
        122.9,
        123.75,
        125.45,
        127.25,
        127.6,
        126.35,
        126.15,
        131.9,
        134.6,
        132.25,
        133.15,
        131.95,
        131.7,
        143.8,
        146.85,
        154.8,
        152.35,
        180.75,
        191.05,
        182,
        187.05,
        182.45,
        184.1,
        182.15,
        183.1,
        176.25,
        185.05,
        206.55,
        205.95,
        206.2,
        219.45,
        220.6,
        212.4,
        192.2,
        208.8,
        208.8,
        216.45,
        221.9,
        220.85,
        221.8,
        228.4,
        232.85,
        227.6,
        229.65,
        238.35,
        236.8,
        237.25,
        228.85,
        230.15,
        224.1,
        216.45,
        217.1,
        260.5,
        273.35,
        261.8,
        253.7,
        282.75,
        280.1,
        306.55,
        303.2,
        248.8,
        261.1,
        254.05,
        268.45,
        263.05,
        256.5,
        252.1,
        248.75,
        247.5,
        243,
        243.65,
        250.5,
        247.4,
        248.2,
        250,
        246.2,
        243.45,
        239.8,
        232.15,
        233.7,
        234.2,
        230.85,
        242.65,
        254.85,
        253.9,
        245.4,
        241.2,
        242.8,
        253.15,
        249.45,
        247.9,
        246.4,
        241.85,
        243.9,
        239.1,
        237.9,
        244.2,
        243,
        241.35,
        241,
        228.9,
        231.05,
        232.6,
        228.95,
        224,
        220.9,
        218.85,
    )
    min_price = stock_trace[0]
    max_profit = 0
    current_profit = 0
    for i, current_price in enumerate(stock_trace[1:], start=1):
        if min_price > current_price:
            min_price = current_price
        current_profit = current_price - min_price
        if current_profit > max_profit:
            max_profit = current_profit

    ic(max_profit)


if __name__ == '__main__':
    main()
