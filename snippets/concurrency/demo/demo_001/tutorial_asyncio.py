import asyncio
import random
import time

from helper import sync_function


async def parallel_function(lock: asyncio.Lock):
    sleep_time: float = random.random() * 5
    print(f"sleeping for {sleep_time:.3f}.")
    await asyncio.sleep(sleep_time)
    async with lock:
        sync_function(sleep_time, "A")
    print(f"=> A exiting after {sleep_time:.3f} seconds")


async def async_demo():
    start = time.perf_counter()
    print("Program starts.")
    lock = asyncio.Lock()
    await asyncio.gather(*(parallel_function(lock) for _ in range(10)))
    end = time.perf_counter()
    print(end - start, "microseconds")
    print("Program ends.")
