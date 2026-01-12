import asyncio
from multiprocessing import Process

import tutorial_asyncio as tutorial_asyncio
import tutorial_multiprocessing
import tutorial_threading as tutorial_threading


async def main():
    await tutorial_asyncio.async_demo()
    process_1 = Process(target=tutorial_threading.threading_demo)
    process_1.start()
    process_2 = Process(target=tutorial_multiprocessing.threading_demo)
    process_2.start()
    process_1.join()
    process_2.join()


if __name__ == '__main__':
    asyncio.run(main())
