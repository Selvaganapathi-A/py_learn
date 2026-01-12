import multiprocessing as mp
import os
import time
from multiprocessing import Pool
from multiprocessing.synchronize import Lock

# Global — visible to all workers after initializer runs
ctx = mp.get_context()
lock: Lock = Lock(ctx=ctx)


def init_worker(some_arg: int):
    print('Process Pool initialized.', some_arg)


def task(arg: tuple[int, int]):
    global lock
    i, j = arg
    with lock:
        print(f'Locked by worker for task {i}')
        time.sleep(3)
        print(f'Lock Released by worker for task {i}')
    # time.sleep(2.0)
    time.sleep(4)
    return j, i


if __name__ == '__main__':
    NUMBER_OF_PROCESSOR: int = os.cpu_count() or 1
    work = tuple((x, x + 50) for x in range(32))
    print('Available Processor', NUMBER_OF_PROCESSOR)
    with Pool(
        processes=NUMBER_OF_PROCESSOR, initializer=init_worker, initargs=(56,)
    ) as pool:
        # consume results as they produced.
        for result in pool.imap_unordered(task, iterable=work):
            print('Result:', result)

        # consume only when all the work are finshed.
        results = pool.map(task, work)
        print(results)
