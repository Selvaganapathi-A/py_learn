from collections import defaultdict

cash_available: dict[int, int] = {
    500: 10,
    200: 100,
    100: 100,
    50: 300,
    20: 100,
    10: 400,
    5: 500,
    2: 500,
    1: 500,
}


def money_dispense(bill: int, given: dict[int, int]):
    logging.debug(f'Bill Amount : {bill: >8}')
    order_of_dispense = (500, 200, 100, 50, 20, 10, 5, 2, 1)
    given_amount: int = 0

    balance = defaultdict(int)

    for rupee, count in given.items():
        logging.debug(f'{rupee: ^9} x {count: ^9}')
        cash_available[rupee] += count
        given_amount += rupee * count
    logging.debug(f'Cash in : Rs.{given_amount}/-')

    remaining = remaining_balance = given_amount - bill
    if remaining_balance < 0:
        raise ValueError('Insufficient Cash')

    # print(given_amount, bill, remaining_balance)

    logging.debug(f'Cash out : Rs.{remaining_balance}/-')
    for rupee in order_of_dispense:
        denomination_count = 0
        while True:
            if remaining == 0 or remaining < rupee:
                break
            if cash_available[rupee] < 1:
                raise ValueError('Not Enough bills.')
            cash_available[rupee] -= 1
            remaining = remaining - rupee
            balance[rupee] += 1
            denomination_count += 1
        if denomination_count != 0:
            logging.debug(f'{rupee: ^9} x {denomination_count: ^9}')
    # print(available_cash())
    return remaining_balance, balance


def available_cash():
    total: int = 0
    for rupee, count in cash_available.items():
        total += rupee * count
    return total


def main():
    print(available_cash())
    print(money_dispense(435, {500: 1}))
    print(money_dispense(127, {100: 1, 50: 1}))
    print(money_dispense(499, {200: 1, 100: 2, 50: 4}))
    print(money_dispense(7287, {500: 16}))
    print(available_cash())
    print(cash_available)


if __name__ == '__main__':
    import logging
    import os

    logging.basicConfig(
        datefmt='%Y-%m-%d %H:%M:%S.%f',
        format='-> {message}',
        style='{',
        level=logging.DEBUG,
    )
    os.system('cls')
    main()
