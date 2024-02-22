import asyncio

# %%
# asyncio  call later


def callback(n):
    print("callback {} invoked".format(n))


async def main(loop):
    print("registering callbacks")
    loop.call_later(0.2, callback, 1)
    loop.call_later(0.1, callback, 2)
    loop.call_soon(callback, 3)

    await asyncio.sleep(5)


event_loop = asyncio.get_event_loop()
try:
    print("entering event loop")
    event_loop.run_until_complete(main(event_loop))
finally:
    print("closing event loop")
    event_loop.close()


# %%
# Pass Croutine to loop call later
async def foo(iv, start):
    await asyncio.sleep(1)
    offset = asyncio.get_running_loop().time() - start
    print(f"done ({offset:.3f}s): {iv}")


async def await_coro_later(delay, coro, *args, **kwargs):
    await asyncio.sleep(delay)
    await coro(*args, **kwargs)


async def demo():
    loop = asyncio.get_running_loop()
    start = loop.time()
    loop.call_later(2, asyncio.create_task, foo("cb_to_create_task", start))
    await await_coro_later(5, foo, "coroutine_call_later", start)


if __name__ == "__main__":
    pass
    asyncio.run(demo())
