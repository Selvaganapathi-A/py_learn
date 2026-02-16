import asyncio
import time


class Paginator:
    def __init__(self, page_size: int) -> None:
        self.__page_size: int = page_size
        self.__start: int = 0
        self.__current_page: int = 1

    def __iter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(0.25)
        page: int = self.__current_page
        start: int = self.__start
        self.__current_page += 1
        self.__start += self.__page_size
        return page, start, self.__page_size + start

    def __aiter__(self):
        return self

    def __next__(self):
        time.sleep(0.25)
        page: int = self.__current_page
        start: int = self.__start
        self.__current_page += 1
        self.__start += self.__page_size
        return page, start, self.__page_size + start


async def async_function(paginator: Paginator):
    print("async function", await anext(paginator))
    print("async function", await anext(paginator))
    print("async function", await anext(paginator))
    print("async function", await anext(paginator))
    print("async function", await anext(paginator))


def sync_function(paginator: Paginator):
    print("sync function", next(paginator))
    print("sync function", next(paginator))
    print("sync function", next(paginator))
    print("sync function", next(paginator))
    print("sync function", next(paginator))


def main():
    paginator = Paginator(100)
    asyncio.run(async_function(paginator))
    sync_function(paginator)


if __name__ == "__main__":
    main()
