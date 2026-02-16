# SuperFastPython.com
# example of using an asyncio semaphore
import asyncio


# task coroutine
async def task(semaphore: asyncio.Semaphore, number: int):
    # acquire the semaphore
    async with semaphore:
        # generate a random value between 0 and 1
        value = 2
        # block for a moment
        await asyncio.sleep(value)
        # report a message
        print(f"Task {number} got {value}")


# main coroutine
async def main():
    # create the shared semaphore
    semaphore = asyncio.Semaphore(3)
    # create and schedule tasks
    async with asyncio.TaskGroup() as taskgroup:
        for _ in range(10):
            _ = taskgroup.create_task(task(semaphore, _))
    #
    # tasks = [asyncio.create_task(task(semaphore, i)) for i in range(10)]
    # # wait for all tasks to complete
    # _ = await asyncio.wait(tasks)


if __name__ == "__main__":
    # start the asyncio program
    asyncio.run(main())
