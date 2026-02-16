import time
from multiprocessing import Lock, Process, Queue


def worker(q, lock, i):
    data = f"Task {i} output"

    # critical section
    with lock:
        q.put(data)
    print("producer exited.", i)


def consumer(q):
    while True:
        item = q.get()
        if item == "STOP":
            break
        print("Consumed:", item)
        time.sleep(1)
    print("consumer exited.")


if __name__ == "__main__":
    q = Queue()
    lock = Lock()

    procs = [Process(target=worker, args=(q, lock, i)) for i in range(4)]
    for p in procs:
        p.start()

    cons = [Process(target=consumer, args=(q,)) for i in range(2)]

    for c in cons:
        c.start()

    for p in procs:
        p.join()

    for c in cons:
        q.put("STOP")

    for c in cons:
        c.join()
