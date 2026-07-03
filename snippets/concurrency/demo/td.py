import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from threading import Lock

lock: Lock = Lock()


def init_worker(some_arg: str):
    print('Thread Pool initialized.', some_arg)


def task(arg: tuple[int, int]):
    global lock
    i, j = arg
    rnc = random.uniform(1, 4)
    with lock:
        print(f'Locked by worker for task {i}')
        time.sleep(rnc)
        print(f'Lock Released by worker for task {i}')
    time.sleep(rnc)
    return Decimal(i + j).quantize(Decimal('1.0'))


if __name__ == '__main__':
    NUMBER_OF_WORKS: int = 4
    NUMBER_OF_THREADS: int = (os.cpu_count() or 1) * 2
    print('Number of Threads used.', NUMBER_OF_THREADS)
    work = tuple((x, x * 100) for x in range(NUMBER_OF_WORKS))
    with ThreadPoolExecutor(
        max_workers=NUMBER_OF_THREADS,
        initializer=init_worker,
        initargs=('ThreadPool',),
    ) as pool:
        for result in pool.map(task, work, chunksize=4):
            print('Result:', result, flush=True)
