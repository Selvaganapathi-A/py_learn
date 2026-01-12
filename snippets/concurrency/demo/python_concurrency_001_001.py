import threading
from time import sleep


def func_001():
    print('func_001 starting')
    sem.acquire()
    for loop in range(1, 5):
        print('func_001 Working {}'.format(loop))
        sleep(1)
    sem.release()
    print('func_001 finished')


def func_002():
    print('fun2 starting')
    while not sem.acquire(blocking=False):
        print('func_002 No Semaphore available')
        sleep(1)
    else:
        print('func_002 got Semphore')
        for loop in range(1, 5):
            print('func_002 Working {}'.format(loop))
            sleep(1)
    sem.release()


def func_003():
    print('func_003 starting')
    while not sem.acquire(blocking=False):
        print('func_003 No Semaphore available')
        sleep(1)
    else:
        print('func_003 got Semphore')
        for loop in range(1, 5):
            print('func_003 Working {}'.format(loop))
            sleep(1)
    sem.release()


if __name__ == '__main__':
    sem = threading.Semaphore(2)
    t1 = threading.Thread(target=func_001)
    t2 = threading.Thread(target=func_002)
    t3 = threading.Thread(target=func_003)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print('All Threads done Exiting')
