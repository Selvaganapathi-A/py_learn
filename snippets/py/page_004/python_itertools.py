def function_01():
    from itertools import batched

    string: list[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    for x in batched(string, n=3):
        print(x)
    print('-' * 80)


def function_02():
    from itertools import zip_longest

    string: list[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    number: list[int] = list(range(9))
    names: list[str] = ['anu', 'mohan', 'priya', 'rahu', 'meera']
    for x in zip_longest(string, number, names):
        print(x)
    print('-' * 80)
    for x in zip_longest(string, number, names, fillvalue=''):
        print(x)
    print('-' * 80)
    for x in zip(string, number, names):
        print(x)
    print('-' * 80)


def function_03():
    from itertools import combinations, pairwise, permutations, product

    string: list[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    names: list[str] = ['anu', 'mohan', 'priya', 'rahu', 'meera']
    for x in product(string, repeat=3):
        print(''.join(x))
    print('-' * 80)
    for x in product(string, names):
        print('-'.join(x))
    print('-' * 80)
    for x in permutations(string, 4):
        print('-'.join(x))
    print('-' * 80)
    for x in combinations(string, 3):
        print('-'.join(x))
    print('-' * 80)
    for x in pairwise(
        string,
    ):
        print(x)
    print('-' * 80)


def function_04():
    def vowel_count(word: str):
        ct: int = 0
        for ch in word:
            if ch in 'aeiou':
                ct += 1
        return ct

    from itertools import groupby

    words: list[str] = [
        'baby',
        'tank',
        'elephant',
        'umbrella',
        'ballon',
        'cat',
        'penguin',
        'google',
        'bing',
        'host',
        'user',
        'android',
        'puma',
        'lion',
        'queensland',
        'kingsland',
        'holland',
    ]
    # returns iterable of consecutive keys based on key function
    sorted_words_by_vowel_count = sorted(words, key=vowel_count)
    grouped_words_by_vowel_count = {
        k: list(v) for k, v in groupby(sorted_words_by_vowel_count, key=vowel_count)
    }
    print(grouped_words_by_vowel_count)


def function_05():
    from itertools import starmap

    rnd_nos = [(1, 2), (3, 2), (4, 6), (8, 3), (7, 5)]
    print(list(starmap(pow, rnd_nos)))


def main():
    function_01()
    function_02()
    function_03()
    function_04()
    function_05()


if __name__ == '__main__':
    main()
