import time


def cache(funct):
    buffer = {}

    def Wrapper(n):
        nonlocal buffer
        if n in buffer:
            return buffer[n]
        else:
            buffer[n] = result = funct(n)
            return result

    return Wrapper


def timeit(funct):
    def Wrapper(*args, **kwargs):
        t1 = time.perf_counter_ns()
        result = funct(*args, **kwargs)
        t2 = time.perf_counter_ns()
        print(f'time to execute : {(t2 - t1)}')
        return result

    return Wrapper


@timeit
@cache
def factorial(n):
    product = 1
    while n > 1:
        product *= n
        n -= 1
    return product


@timeit
@cache
def nth_fibbonocci(n):
    a, b = 0, 1
    while n > 0:
        a, b = b, a + b
        n -= 1
    return a


print(nth_fibbonocci(49))
print(nth_fibbonocci(49))
print(nth_fibbonocci(49))
print(factorial(400))
print(factorial(400))
print(factorial(400))
print(factorial(400))
print(factorial(400))
