import asyncio
from typing import Any, AsyncGenerator, Self


class Async_Iterator[T: (int, float)]:
    def __init__(self, start: T, stop: T, step: T) -> None:
        self.start = start
        self.stop = stop
        self.step = step

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        x: T = self.start
        if self.step > 0:
            if self.start >= self.stop:
                raise StopAsyncIteration(self.start, self.stop)
        elif self.step < 0:
            if self.start < self.stop:
                raise StopAsyncIteration(self.start, self.stop)
        self.start += self.step
        return x


async def Async_Generator[T: (int, float)](
    start: T, stop: T, step: T
) -> AsyncGenerator[T, Any]:
    while start < stop:
        yield start
        start += step


async def main():
    async for x in Async_Iterator(10, 100, 2):
        print(f'{x:4.2f}')
    print()
    # hideit print("#" * 80)
    async for x in Async_Generator(350, 600, 10):
        print(x)
    print()
    # hideit print("#" * 80)
    async for x in Async_Generator(350.78, 600.37, 13.147):
        print(x)
    print()
    # hideit print("#" * 80)


if __name__ == '__main__':
    asyncio.run(main())
