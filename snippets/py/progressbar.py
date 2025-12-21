import queue
import threading
import time
from enum import IntEnum, auto

from rich.live import Live
from rich.progress import BarColumn, Progress, ProgressColumn, TextColumn


class Status(IntEnum):
    error = auto()
    progress = auto()
    done = auto()


def worker(n, q):
    for _ in range(n):
        time.sleep(0.01)
        q.put(Status.progress)
    q.put(Status.done)


def main():
    total = 100
    q: queue.Queue[Status] = queue.Queue(maxsize=100)
    t = threading.Thread(target=worker, args=(total, q), daemon=True)
    t.start()
    with Progress(
        TextColumn('[bold blue]{task.description}'),
        BarColumn(),
        TextColumn('{task.completed}/{task.total}'),
    ) as progress:
        task = progress.add_task('Processing', total=total)
        while True:
            message: Status = q.get()
            if message == Status.done:
                break
            progress.update(task, advance=1)
    t.join()


if __name__ == '__main__':
    main()
