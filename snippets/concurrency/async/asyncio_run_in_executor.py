import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def cpu_heavy_work(i: int, j: int = 8, *, l: str = 'poll'):
    time.sleep(3)
    return i * j


async def sheduler(
    task_count: int,
    semaphore: asyncio.Semaphore,
    eventloop: asyncio.AbstractEventLoop,
    cpupool: ProcessPoolExecutor,
):
    async with semaphore:
        result = await eventloop.run_in_executor(cpupool, partial(cpu_heavy_work, task_count, 1, l='lorem'))
        print(result)
        return


async def main():
    eventloop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=4) as processpool:
        async with asyncio.TaskGroup() as taskgroup:
            semaphore = asyncio.Semaphore(4)
            for task in range(20):
                _ = taskgroup.create_task(
                    sheduler(
                        task + 1,
                        semaphore,
                        eventloop,
                        processpool,
                    )
                )


if __name__ == '__main__':
    asyncio.run(main())
