import asyncio
import secrets
from typing import Iterable, NoReturn, Tuple

import faker
from faker_food import FoodProvider  # type:ignore


async def producer(queue: asyncio.LifoQueue[Tuple[int, float, str]]):
    items: int = 50
    item: int = 0
    sleep_time = tuple(range(10, 101))
    order_ids = list(range(10, items))
    Faker = faker.Faker()
    Faker.add_provider(FoodProvider)
    await asyncio.sleep(1)
    while item < items:
        order_id = secrets.choice(range(len(order_ids) - 1))
        cook_time = secrets.choice(sleep_time) / 10
        food = Faker.dish()
        order = (order_id, cook_time, food)
        print(
            f'{order_id:>3} \x1b[38;5;2mordering',
            food,
            'with',
            cook_time,
            '\x1b[0m',
            flush=True,
        )
        await queue.put(order)
        item += 1
    print('\x1b[48;5;6m' + '#' * 80 + '\x1b[0m', flush=True)


async def consumer(queue: asyncio.LifoQueue[Tuple[int, float, str]]):
    while True:
        order_id, cook_time, food = await queue.get()
        print(f'{order_id:>3} \x1b[38;5;3m   cooking', food, '\x1b[0m', flush=True)
        await asyncio.sleep(cook_time)
        print(
            f'{order_id:>3} \x1b[38;5;9m      served',
            food,
            'in',
            cook_time,
            'minutes.',
            '\x1b[0m',
            flush=True,
        )
        queue.task_done()


async def function():
    QUEUE_SIZE: int = 10
    WORKERS: int = 4
    lifo_queue: asyncio.LifoQueue[Tuple[int, float, str]] = asyncio.LifoQueue(QUEUE_SIZE)
    consumers: Iterable[asyncio.Task[NoReturn]] = list()
    for _ in range(WORKERS):
        task = asyncio.create_task(consumer(lifo_queue))
        consumers.append(task)
    await producer(lifo_queue)
    await lifo_queue.join()
    for consumer_ in consumers:
        consumer_.cancel()


def main():
    asyncio.run(function())


if __name__ == '__main__':
    main()
