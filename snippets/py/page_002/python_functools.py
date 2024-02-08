# Lambda Function
from functools import partial, reduce
from typing import Any, Iterable, Mapping


def styleit(string: str):
    print()
    print(f"# {(' ' + string +' ') .center(76, '*')} #")
    print()


def demo_filter():
    styleit("Filter Example")
    numbers: Iterable[int] = [x for x in range(1, 100)]
    #
    print(f"Numbers :\n\t{numbers}".expandtabs(4))
    #
    nums_divisible_by_7: Iterable[int] = tuple(
        filter(lambda x: (x % 7) == 0, numbers)
    )
    print(f"Numbers Divide by 7 :\n\t{nums_divisible_by_7}".expandtabs(4))
    pass


def demo_reduce():
    styleit("Reduce Example")
    natural_numbers: Iterable[int] = [x for x in range(1, 4)]
    #
    sum_of_nums = reduce(lambda x, y: x + y, natural_numbers)
    #
    print(f"Numbers :\n\t{natural_numbers}".expandtabs(4))
    print(f"sum of numbers = {sum_of_nums}")
    #
    pass


def demo_map():
    styleit("Map Example")
    #
    natural_numbers: Iterable[int] = [x for x in range(1, 11)]
    #
    print(f"Numbers :\n\t{natural_numbers}".expandtabs(4))
    #
    multiply_by_five = tuple(map(lambda x: x * 5, natural_numbers))
    print(f"Multiply Each Number by Five\n\t{multiply_by_five}".expandtabs(4))
    #
    pass


def demo_partial():
    styleit("Partial Example")

    # partial Example
    def gamer(
        name: str, level: int = 0, experience: int = 0
    ) -> Mapping[str, Any]:
        return {"name": name, "level": level, "exp": experience}

    level_80 = partial(gamer, level=80)
    experience_76 = partial(gamer, experience=76)

    print(level_80("aadhi"))
    print(experience_76("varun"))
    print(experience_76("ganga", experience=90, level=44))
    pass


def main():
    demo_filter()
    print()
    demo_map()
    print()
    demo_reduce()
    print()
    demo_partial()
    print()


if __name__ == "__main__":
    main()
