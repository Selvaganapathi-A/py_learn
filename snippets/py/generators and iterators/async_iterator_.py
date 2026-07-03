import asyncio
from decimal import Decimal
from typing import Self


class AsyncIterator[T: (int, float, Decimal)]:
    def __init__(self, start: T, stop: T, step: T) -> None:
        self.start: T = start
        self.stop: T = stop
        self.step: T = step
        self.incremental: bool = start < stop
        if step == 0:
            error_message = "Can't Iterate with `0` steps."
            raise ValueError(error_message)
        if (self.incremental and step < 0) or (not self.incremental and step > 0):
            error_message = f'Invalid range [{start=}, {stop=}, {step=}].'
            raise ValueError(error_message)

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        x: T = self.start
        if self.incremental:
            if self.start >= self.stop:
                raise StopAsyncIteration(self.start, self.stop)
        elif self.start < self.stop:
            raise StopAsyncIteration(self.start, self.stop)
        self.start += self.step
        return x


async def main() -> None:
    async for x in AsyncIterator[int](10, 30, 7):
        print(f'{x:4.2f}')


if __name__ == '__main__':
    asyncio.run(main())
