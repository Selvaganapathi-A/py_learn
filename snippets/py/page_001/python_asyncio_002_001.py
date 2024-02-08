import asyncio
import logging


async def foo() -> str:
    await asyncio.sleep(1.5)
    return "foo"


async def bar() -> str:
    await asyncio.sleep(0.5)
    print(1 / 0)
    return "bar"


async def main():
    task1 = asyncio.create_task(foo(), name="foo function")
    task2 = asyncio.create_task(bar(), name="bar function")

    done, pending = await asyncio.wait(
        (task1, task2), return_when=asyncio.ALL_COMPLETED
    )

    print("-" * 80)

    print("Task Completed.")
    for task in done:
        try:
            print((task, task.get_name(), task.result()))
        except Exception as e:
            print((task, task.get_name()))
            logging.exception(e, exc_info=e)
        print()

    print("-" * 80)

    print("Task Pending.")
    for task in pending:
        print((task, task.get_name(), task.result()))
        print()

    print("-" * 80)


if __name__ == "__main__":
    asyncio.run(main=main())
