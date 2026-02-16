import random
import time
from multiprocessing import Process, get_context
from multiprocessing.synchronize import Lock

from helper import sync_function


def parallel_function(lock: Lock):
    sleep_time: float = random.random() * 5
    print(f"sleeping for {sleep_time:.3f}.")
    time.sleep(sleep_time)
    with lock:
        sync_function(sleep_time, "P")
    print(f"=> P exiting after {sleep_time:.3f} seconds")


def threading_demo():
    start = time.perf_counter()
    print("Program starts.")
    lock: Lock = Lock(ctx=get_context(method="spawn"))
    processes: list[Process] = []
    # print(type(lock))
    for _ in range(10):
        process = Process(target=parallel_function, args=(lock,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end = time.perf_counter()
    print(end - start, "microseconds")
    print("Program ends.")
