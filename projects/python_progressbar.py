import time
from random import randint, random
from time import sleep

from tqdm import tqdm, trange


def main():
    with trange(10) as t:
        for i in t:
            # Description will be displayed on the left
            t.set_description('GEN %i' % i)
            # Postfix will be displayed on the right,
            # formatted automatically based on argument's datatype
            t.set_postfix(
                loss=random(),
                gen=randint(1, 999),
                str='h',
                lst=[1, 2],
            )
            sleep(0.1)

    with tqdm(
        total=10,
        bar_format='{postfix[0]} {bar} {postfix[1][value]:>8.2f} {postfix[2]} {postfix[3]}',
        postfix=['Batch', {'value': 0}, '', ''],
    ) as t:
        for i in range(101):
            sleep(0.1)
            t.postfix[1]['value'] = i / 4
            t.postfix[2] = i / 2
            t.postfix[3] = i
            t.update()

    for _ in tqdm(range(1, 26, 1)):
        time.sleep(1)


"""
bar_format  : str, optional
|          Specify a custom bar string formatting. May impact performance.
|          [default: '{l_bar}{bar}{r_bar}'], where
|          l_bar='{desc}: {percentage:3.0f}%|' and
|          r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
|            '{rate_fmt}{postfix}]'
|          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
|            percentage, elapsed, elapsed_s, ncols, nrows, desc, unit,
|            rate, rate_fmt, rate_noinv, rate_noinv_fmt,
|            rate_inv, rate_inv_fmt, postfix, unit_divisor,
|            remaining, remaining_s, eta.
|          Note that a trailing ": " is automatically removed after {desc}
|          if the latter is empty.
"""

if __name__ == '__main__':
    # main()
    # help(tqdm)
    # ┳░▒▒▓█▀▄▁▂▃▄▅▆▇█▉
    print('┳░▒▓█▀▄▁▂▃▄▅▆▇█▉ ┏┛┗┓┣┳┻━╋━┻┳┫╏╭╯╰╮')
    with tqdm(
        total=10,
        bar_format='{percentage:6.2f} % {bar} ',
        postfix=' ',
        ascii='░█',
        colour='Blue',
    ) as t:
        for j in range(1, 11):
            sleep(0.1)
            t.update()
