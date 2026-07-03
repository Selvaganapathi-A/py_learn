import asyncio
from decimal import Decimal
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


async def asynchronous_generator[T: (int, float, Decimal)](start: T, stop: T, step: T) -> AsyncGenerator[T]:
    next_val: T = start
    while next_val < stop:
        yield next_val
        next_val = cast('T', next_val + step)
        await asyncio.sleep(0.25)


async def main() -> None:
    async for x in asynchronous_generator(1.1, 11.11, 2.31):
        print(x)
    print('#' * 80)


if __name__ == '__main__':
    asyncio.run(main())
