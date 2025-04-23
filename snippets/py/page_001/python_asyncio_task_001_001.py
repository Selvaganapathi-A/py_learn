# from collections.abc import Coroutine
import asyncio
import random
from typing import Coroutine


async def coro(a: int, b: 'str'):
    await asyncio.sleep(a)
    print(b)
    return (b + ' ') * (a + 1)


async def main():
    help(Coroutine)
    tasks: list[asyncio.Task[str]] = list()
    for x in range(10):
        task = asyncio.create_task(coro(random.randint(3, 9), chr(65 + x)),
                                   name='goku')
        tasks.append(task)
    resuly = await asyncio.gather(*tasks)
    print(resuly)
    print('Program finished.')


if __name__ == '__main__':
    asyncio.run(main())
