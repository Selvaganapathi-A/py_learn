import random
import threading
import time

from helper import sync_function


def parallel_function(lock: threading.Lock):
    sleep_time: float = random.random() * 5
    print(f'sleeping for {sleep_time:.3f}.')
    time.sleep(sleep_time)
    with lock:
        sync_function(sleep_time, 'T')
    print(f'=> T exiting after {sleep_time:.3f} seconds')


def threading_demo():
    start = time.perf_counter()
    print('Program starts.')
    lock = threading.Lock()
    threads: list[threading.Thread] = []
    # create and start threads.
    for _ in range(10):
        t = threading.Thread(target=parallel_function, kwargs={'lock': lock})
        threads.append(t)
        t.start()
    # wait for other threads to finish.
    for t in threads:
        t.join()
    end = time.perf_counter()
    print(end - start, 'microseconds')
    print('Program ends.')
