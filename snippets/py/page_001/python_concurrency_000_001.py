from concurrent.futures import as_completed, ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
from typing import Any, List

# ~ # filename : learn - thread pool executor.py
import datetime
import os
import time


def Threadfunc():
    timestamp = datetime.datetime.now()
    time.sleep(1)
    return (
        current_thread().name,
        datetime.datetime.now(),
        timestamp,
    )


def Processfunc():
    timestamp = datetime.datetime.now()
    time.sleep(1)
    return (
        current_thread().name,
        datetime.datetime.now(),
        timestamp,
    )


def fn_name(name: str) -> str:
    time.sleep(1)
    return name + " 5"


if __name__ == "__main__":
    names = [
        "alpha",
        "bravo",
        "charlie",
        "delta",
        "echo",
        "foxtrot",
        "golf",
        "hotel",
        "india",
        "juliet",
    ]
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as Executor:
        future_object = (
            Executor.submit(
                fn_name,
                x,
            )
            for x in names
        )
        for x in as_completed(future_object):
            print(x.result())
    #
    print()
    #
    timestamp = datetime.datetime.now()
    with ThreadPoolExecutor(4, "Miami") as Executor:
        r: List[Any] = []
        for x in range(16):
            r.append(Executor.submit(Threadfunc))
        Executor.shutdown(wait=True)
        for x in r:
            m, n, o = x.result()
            print(m, n - o)
        print(
            "Threadpool Completed",
            datetime.datetime.now() - timestamp,
        )
    #
    print()
    #
    timestamp = datetime.datetime.now()
    with ProcessPoolExecutor(4) as Executor:
        r: List[Any] = []
        for x in range(16):
            r.append(Executor.submit(Processfunc))
        Executor.shutdown(wait=True)
        for x in r:
            m, n, o = x.result()
            print(m, n - o)
        print(
            "ProcessPool Completed",
            datetime.datetime.now() - timestamp,
        )
