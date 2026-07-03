import time
from collections.abc import Generator


def twine(start: float, stop: float, step: float) -> Generator[float, float]:
    value: float
    current: float = start

    while True:
        if (start < stop < current) or (start > stop > current):
            break
        value = yield current
        if isinstance(value, float):
            if ((start < stop) and (value > 0)) or ((start > stop) and (value < 0)):
                step = value
            else:
                raise UnboundLocalError
            print('received new step value', value)
        current += step


def main() -> None:
    thingy = twine(-10.0, 100.0, 1.125)
    error_throw_at: float = 90.73
    stop_at: float = 40.73
    change_step_at: float = 20.73

    while True:
        try:
            value = next(thingy)
            print(value)
            if value > change_step_at:
                # ! Example to 'send' Method
                thingy.send(2.250)
            if value > error_throw_at:
                # ! Example to 'throw' Method
                thingy.throw(ValueError('Hello Google'))
            if value > stop_at:
                # ! Example to 'close' Method
                thingy.close()
        except StopIteration as se:
            print(se)
            break
        except KeyboardInterrupt:
            return
        time.sleep(0.1)
    print('End of Program')


if __name__ == '__main__':
    main()
