class A:
    def __init__(self) -> None:
        print('A Initialized.')
        super().__init__()
        super().__init_subclass__()

    def function(self):
        print('A ouject function called.')


class B(A):
    def __init__(self) -> None:
        print('B Initialized.')
        super().__init__()
        super().__init_subclass__()

    def function(self):
        print('B ouject function called.')
        super().function()


class BA(B):
    def __init__(self) -> None:
        print('BA Initialized.')
        super().__init__()
        super().__init_subclass__()

    def function(self):
        print('BA [B, A] ouject function called.')
        super().function()


class BBA(BA):
    def __init__(self) -> None:
        print('BA B A Initialized.')
        super().__init__()
        super(BBA, self).__init_subclass__()

    def function(self):
        print('BBA [BA, B, A] ouject function called.')
        super().function()


def main():
    bba = BBA()
    bba.function()
    print(bba.__class__.__bases__)


if __name__ == '__main__':
    main()
