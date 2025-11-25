# Lambda Function
from collections.abc import Iterable, Mapping
from functools import partial, reduce
from typing import Any


def styleit(string: str):
    print(f'# {(" " + string + " ").center(76, "*")} #')


def demo_filter():
    styleit('Filter Example')
    numbers: Iterable[int] = list(range(1, 100))
    print(f'Numbers :\n\t{numbers}'.expandtabs(4))
    nums_divisible_by_7: Iterable[int] = tuple(
        filter(lambda x: (x % 7) == 0, numbers)
    )
    print(f'Numbers Divide by 7 :\n\t{nums_divisible_by_7}'.expandtabs(4))


def demo_reduce():
    styleit('Reduce Example')
    natural_numbers: Iterable[int] = list(range(1, 4))
    sum_of_nums = reduce(lambda x, y: x + y, natural_numbers)
    print(f'Numbers :\n\t{natural_numbers}'.expandtabs(4))
    print(f'sum of numbers = {sum_of_nums}')


def demo_map():
    styleit('Map Example')
    natural_numbers: Iterable[int] = list(range(1, 11))
    print(f'Numbers :\n\t{natural_numbers}'.expandtabs(4))
    multiply_by_five = tuple((x * 5 for x in natural_numbers))
    print(f'Multiply Each Number by Five\n\t{multiply_by_five}'.expandtabs(4))


def demo_partial():
    styleit('Partial Example')

    # partial Example
    def gamer(
        name: str, level: int = 0, experience: int = 0
    ) -> Mapping[str, Any]:
        return {'name': name, 'level': level, 'exp': experience}

    level_80 = partial(gamer, level=80)
    experience_76 = partial(gamer, experience=76)
    print(level_80('aadhi'))
    print(experience_76('varun'))
    print(experience_76('ganga', experience=90, level=44))


def main():
    demo_filter()
    demo_map()
    demo_reduce()
    demo_partial()


if __name__ == '__main__':
    main()
