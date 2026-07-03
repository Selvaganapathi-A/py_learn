import time
from types import TracebackType
from typing import Any


class AsyncCustomContextManager:
    async def __aenter__(self):
        self.start = time.perf_counter()
        print('entering')
        return self

    async def __aexit__(
        self,
        exception: Exception,
        message: Any,
        traceback: TracebackType,
    ):
        end = time.perf_counter()
        print(end - self.start, 'microseconds in async mode')
        # Exception Propagation if return False or
        #     suppress particular exception with `isinstance` method
        return False


async def main():
    import asyncio

    async with AsyncCustomContextManager():
        for _ in range(5):
            print('->', _)
            await asyncio.sleep(0.1)
        print(81 / 0)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
