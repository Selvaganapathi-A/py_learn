import logging
import time
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(format="{message}", style="{", level=10)


def function():
    time.sleep(2)
    return 3


def main():
    start = time.monotonic()

    with ThreadPoolExecutor(4) as threadpool:
        task_list = (threadpool.submit(function) for _ in range(8))
        for task in task_list:
            task.add_done_callback(lambda task_: logging.info("ended = %d", task_.result()))

    end = time.monotonic()
    logging.info("Threadpool = %f", end - start)

    start = time.monotonic()
    function()
    function()
    function()
    end = time.monotonic()
    logging.info("main = %f", end - start)


if __name__ == "__main__":
    main()
