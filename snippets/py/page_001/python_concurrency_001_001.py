import threading
from time import sleep


def fun1():
    print("fun1 starting")
    sem.acquire()
    for loop in range(1, 5):
        print("Fun1 Working {}".format(loop))
        sleep(1)
    sem.release()
    print("fun1 finished")


def fun2():
    print("fun2 starting")
    while not sem.acquire(blocking=False):
        print("Fun2 No Semaphore available")
        sleep(1)
    else:
        print("Got Semphore")
        for loop in range(1, 5):
            print("Fun2 Working {}".format(loop))
            sleep(1)
    sem.release()


def fun3():
    print("fun3 starting")
    while not sem.acquire(blocking=False):
        print("Fun3 No Semaphore available")
        sleep(1)
    else:
        print("Got Semphore")
        for loop in range(1, 5):
            print("Fun3 Working {}".format(loop))
            sleep(1)
    sem.release()


if __name__ == "__main__":
    sem = threading.Semaphore()
    t1 = threading.Thread(target=fun1)
    t2 = threading.Thread(target=fun2)
    t3 = threading.Thread(target=fun3)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print("All Threads done Exiting")
