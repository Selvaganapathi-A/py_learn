import asyncio
from typing import NoReturn


async def producer(queue: asyncio.Queue[tuple[str, int]], task_id: str):
    for x in range(11, 21):
        await queue.put((task_id, x))
        await asyncio.sleep(0.2)


async def consumer(queue: asyncio.Queue[tuple[str, int]], task_id: str):
    while True:
        prod_id, value = await queue.get()
        print(
            f'\x1b[38;5;{len(task_id)}m{task_id:>20}\x1b[0m {value:^4} {prod_id}'
        )
        queue.task_done()
        await asyncio.sleep(1)


async def main():
    llms = ['cisco', 'intel', 'samsung', 'mediatek', 'snapdragon', 'nvidia']
    countries = [
        'iran',
        'china',
        'urgentina',
        'brazil',
        'iraq',
        'saudi',
        'peru',
        'spain',
        'london',
    ]
    queue: asyncio.Queue[tuple[str, int]] = asyncio.Queue(3)
    # * create list to track tasks.
    producers: list[asyncio.Task[None]] = list()
    for task_id in countries:
        task = asyncio.create_task(producer(queue, task_id), name=task_id)
        producers.append(task)
    # * create list to track tasks.
    consumers: list[asyncio.Task[NoReturn]] = list()
    for task_id in llms:
        task = asyncio.create_task(consumer(queue, task_id), name=task_id)
        consumers.append(task)
    # * wait for tasks to finish
    await asyncio.wait(producers)
    # * cancel all tasks
    for task in producers:
        task.cancel()
    # * cancel all tasks
    for task in consumers:
        task.cancel()


if __name__ == '__main__':
    asyncio.run(main())
