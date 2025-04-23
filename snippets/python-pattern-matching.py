from typing import Any


def comparer(data: Any):
    # print(data)
    match data:
        case {'a': int()}:
            print('inti')
        case {'z': float()}:
            print('floati')
        case _:
            print('unknowni')


def main():
    data_1 = {'a': 1, 'b': 3, 'd': '5'}
    data_2 = {'a': '1', 'b': 3, 'd': '5'}
    data_3 = {'a': '1', 'b': 3, 'z': 3.14}
    comparer(data_1)
    comparer(data_2)
    comparer(data_3)


if __name__ == '__main__':
    main()
