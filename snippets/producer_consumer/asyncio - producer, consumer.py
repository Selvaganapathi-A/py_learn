from typing import NoReturn

import asyncio


async def produce(queue: asyncio.Queue[int], n: int):
    for x in range(1, n + 1):
        # produce an item
        print(f'producing {x}/{n}')
        # simulate i/o operation using sleep
        await asyncio.sleep(2)
        # put the item in the queue
        await queue.put(x)


async def consume(queue: asyncio.Queue[int]):
    while True:
        # wait for an item from the producer
        item = await queue.get()

        # process the item
        print(f'consuming {item}...')
        # simulate i/o operation using sleep
        await asyncio.sleep(5)

        # Notify the queue that the item has been processed
        queue.task_done()


async def run(n: int):
    queue: asyncio.Queue[int] = asyncio.Queue()

    # schedule consumers
    consumers: list[asyncio.Task[NoReturn]] = [
        asyncio.create_task(consume(queue)) for _ in range(3)
    ]

    # run the producer and wait for completion
    await produce(queue, n)
    # wait until the consumer has processed all items
    await queue.join()

    # the consumers are still awaiting for an item, cancel them
    for consumer in consumers:
        consumer.cancel()

    # wait until all worker tasks are cancelled
    await asyncio.gather(*consumers, return_exceptions=True)


def main():
    asyncio.run(run(10))
    pass


if __name__ == "__main__":
    main()
    pass
