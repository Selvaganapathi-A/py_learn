from typing import Self


class Range[T: (int, float)]:
    def __init__(self, *args: T) -> None:
        start: T
        stop: T
        step: T
        if len(args) == 1:
            start = 0  # type: ignore
            stop = args[0]
            step = 1  # type: ignore
        elif len(args) == 2:
            start, stop = args
            step = 1  # type: ignore
        elif len(args) == 3:
            start, stop, step = args
        else:
            raise ValueError(*args)
        self.__current: T = start
        self.__start: T = start
        self.__stop: T = stop
        self.__step: T = step

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> T:
        current = self.__current
        if self.__current > self.__stop:
            raise StopIteration(self.__start, self.__stop, self.__step)
        self.__current = self.__current + self.__step
        return current
