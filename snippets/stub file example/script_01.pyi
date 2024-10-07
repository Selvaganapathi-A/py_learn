from typing import overload, Self

class Range[T: (int, float)]:
    """
    ## Range (stop)
    iterate from `start = 0` upto `stop` value
    with each `step = 1`

    ## Range (start, stop)
    iterate from `start` to `stop`
    with each `step = 1`

    ## Range (start, stop, step)
    iterate from `start` to `stop`
    with each `step`
    """

    @overload
    def __init__(self, stop: T) -> None: ...
    @overload
    def __init__(self, start: T, stop: T) -> None: ...
    @overload
    def __init__(self, start: T, stop: T, step: T) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> T: ...
