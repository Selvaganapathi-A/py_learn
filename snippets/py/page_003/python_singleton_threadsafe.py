import time
from threading import Lock, Thread
from typing import Any


class Singleton(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class someclass(metaclass=Singleton): ...


class NaiveSingleton(type):
    __naive_instances__: dict[Any, Any] = {}
    __threadLock__ = Lock()

    def __call__(cls, *args, **kwargs):
        with cls.__threadLock__:
            if cls not in cls.__naive_instances__:
                cls.__naive_instances__[cls] = super().__call__(*args, **kwargs)
        return cls.__naive_instances__[cls]


class Entertainment(metaclass=NaiveSingleton):
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs


def test_singleton(*args, lock: Lock, **kwargs):
    lock.acquire()
    time.sleep(0.5)
    print(args)
    time.sleep(0.5)
    print(kwargs)
    time.sleep(0.5)
    device = Entertainment(*args, **kwargs)
    print(device.args)
    time.sleep(0.5)
    print(device.kwargs)
    time.sleep(0.5)
    lock.release()


if __name__ == '__main__':
    lock = Lock()
    t1 = Thread(
        target=test_singleton,
        args=('speaker', 'play songs'),
        kwargs={'lock': lock, 'device_id': 8979, 'thrread': 1},
    )
    # t1.daemon = True
    t2 = Thread(
        target=test_singleton,
        args=('mobile', 'blood sucker'),
        kwargs={'lock': lock, 'device_id': 4552, 'thrread': 2},
    )
    # t2.daemon = True
    t2.start()
    t1.start()
    t1.join()
    t2.join()
