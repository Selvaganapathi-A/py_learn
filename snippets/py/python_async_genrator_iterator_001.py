import asyncio
from collections.abc import AsyncGenerator
from decimal import Decimal
from typing import Any, Self


class Async_Iterator[T: (int, float, Decimal)]:
    def __init__(self, start: T, stop: T, step: T) -> None:
        self.start = start
        self.stop = stop
        self.step = step
        #
        self.incremental: bool = start < stop
        if step == 0:
            raise ValueError("Can't Iterate with `0` steps.")
        if (self.incremental and step < 0) or (
            not self.incremental and 0 < step
        ):
            raise ValueError('Invalid range.', start, stop, step)

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        x: T = self.start
        if self.incremental:
            if self.start >= self.stop:
                raise StopAsyncIteration(self.start, self.stop)
        else:
            if self.start < self.stop:
                raise StopAsyncIteration(self.start, self.stop)
        self.start += self.step
        return x


async def Async_Generator[T: (int, float, Decimal)](
    start: T, stop: T, step: T
) -> AsyncGenerator[T, Any]:
    while start < stop:
        yield start
        start += step


async def main():
    async for x in Async_Iterator[int](10, 30, 7):
        print(f'{x:4.2f}')
    print('#' * 80)
    async for x in Async_Generator(350, 500, 23):
        print(x)
    print('#' * 80)
    async for x in Async_Generator(
        Decimal('350.78'), Decimal('500.37'), Decimal(' 13.147')
    ):
        print(x)
    print('#' * 80)


if __name__ == '__main__':
    asyncio.run(main())
