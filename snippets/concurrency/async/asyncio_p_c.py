import asyncio

from rich import print as console


async def _producer(
    out_queue: asyncio.PriorityQueue[tuple[int, int]],
) -> None:
    for i in range(100):
        priority = (i % 16) + 1
        await out_queue.put((priority, i))
        console(f"[red]produce {priority: >3d} {i: >3d}[/red]")
    out_queue.shutdown()


async def _consumer(
    in_queue: asyncio.PriorityQueue[tuple[int, int]],
    concurrency_control: asyncio.Semaphore,
    worker_name: str,
) -> None:
    while True:
        try:
            """Wait until the item arrived or queue shutdown is triggered in upstream."""
            priority, task = await in_queue.get()
        except asyncio.QueueShutDown:
            break
        """Only allows n number of tasks are allowed to execute following code despite 100s of consumer running concurrently"""
        async with concurrency_control:
            console(
                f"[cyan]worker: {worker_name: >3s}[/cyan] [green]priority : {priority: > 3d} & Task : {task}[/green]"
            )
            await asyncio.sleep(0.5)
        in_queue.task_done()


async def main() -> None:
    """### Producer Consumer Demo.

    Non blocking and non polling version of Async pipeline management.
    """
    queue: asyncio.PriorityQueue[tuple[int, int]] = asyncio.PriorityQueue(maxsize=32)
    concurrency_control = asyncio.Semaphore(4)
    async with asyncio.TaskGroup() as taskgroup:
        taskgroup.create_task(_producer(queue))
        for i in range(32):
            taskgroup.create_task(
                _consumer(queue, concurrency_control, worker_name=f"{i}")
            )


if __name__ == "__main__":
    asyncio.run(main())
