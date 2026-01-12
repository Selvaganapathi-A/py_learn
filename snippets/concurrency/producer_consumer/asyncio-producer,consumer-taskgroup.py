import asyncio
import dataclasses
import random

from colorama import Fore


@dataclasses.dataclass(slots=True)
class Control[T]:
    lock: asyncio.Lock
    inflight: asyncio.Semaphore
    queue: asyncio.Queue[T]
    workers: int
    pressure: int = 0
    events: list[asyncio.Event] = dataclasses.field(
        init=False, default_factory=lambda: list[asyncio.Event]()
    )

    def __post_init__(self):
        for worker in range(self.workers):
            self.events.append(asyncio.Event())

    async def finished(self):
        async with self.lock:
            return (
                all(event.is_set() for event in self.events)
                and self.queue.empty()
            )

    async def set_event(self):
        async with self.lock:
            for event in self.events:
                if not event.is_set():
                    event.set()
                    break


def sleep():
    return random.uniform(0.01, 0.1)


@dataclasses.dataclass(slots=True, kw_only=True)
class WorkItem:
    item: int


async def produce(producer_id: int, control_out: Control[WorkItem], n: int):
    for x in range(1, n + 1):
        # simulate i/o operation using sleep
        await asyncio.sleep(sleep())
        #
        await control_out.inflight.acquire()
        # put the item in the queue
        await control_out.queue.put(WorkItem(item=x))
        #
        print(
            (
                f'{Fore.RED}[x] {producer_id: >3d} - producing '
                f'{x}/{n}{Fore.RESET}'
            )
        )

    await control_out.set_event()
    print(f'{producer_id} Producer exits.')


async def processor(
    stage: int,
    processor_id: int,
    control_in: Control[WorkItem],
    control_out: Control[WorkItem],
):
    while True:
        try:
            # wait for an item from the producer
            item = await asyncio.wait_for(control_in.queue.get(), 0.5)
        except asyncio.TimeoutError:
            if await control_in.finished():
                break
            # print(
            #     'Processor Stage',
            #     stage,
            #     consumer_id,
            #     'Worker running ideal.',
            #     id(control_in),
            #     id(control_out),
            # )
            continue
        try:
            # simulate i/o operation using sleep
            await asyncio.sleep(sleep())
            # put the item into queue
            await control_out.queue.put(item)
            #
            txt = ('   ' * stage) + '[x]'
            print(
                (
                    f'{Fore.YELLOW}{txt} {processor_id: >3d}'
                    f' - processing {item.item}...{Fore.RESET}'
                )
            )
        finally:
            # Notify the queue that the item has been processed
            control_in.queue.task_done()
    # print(f'Processor {consumer_id} exit.')
    await control_out.set_event()


async def sink(
    stage: int,
    sink_id: int,
    sink_control: Control[WorkItem],
):
    while True:
        try:
            # wait for an item from the producer
            item = await asyncio.wait_for(sink_control.queue.get(), 0.5)
        except asyncio.TimeoutError:
            if await sink_control.finished():
                break
            # print(
            #     'Sink of Stage',
            #     stage,
            #     consumer_id,
            #     'Worker running ideal.',
            #     id(control_in),
            # )
            continue
        try:
            # simulate i/o operation using sleep
            await asyncio.sleep(sleep())
            # consume the item
            txt = ('   ' * stage) + '[x]'
            print(
                (
                    f'{Fore.CYAN}{txt} {sink_id: >3d} - consuming '
                    f'{item.item}...{Fore.RESET}'
                )
            )
        finally:
            # Notify the queue that the item has been processed
            sink_control.queue.task_done()
            # reloase inflight control to produce more item.
            sink_control.inflight.release()


async def run(n: int):
    number_of_stages = 3
    #
    number_of_producers = 1
    number_of_processers = 4
    number_of_consumers = 3
    #
    max_queue_size = 12
    inflight = 8
    #
    sem = asyncio.Semaphore(inflight)
    controls: list[Control[WorkItem]] = [
        Control(
            lock=asyncio.Lock(),
            inflight=sem,
            queue=asyncio.Queue[WorkItem](maxsize=max_queue_size),
            workers=number_of_producers if i == 0 else number_of_processers,
        )
        for i in range(number_of_stages + 1)
    ]

    # return
    async with asyncio.TaskGroup() as taskgroup:
        # run the producer and wait for completion
        for producer_id in range(number_of_producers):
            taskgroup.create_task(
                produce(
                    producer_id,
                    controls[0],
                    n,
                )
            )
        #
        for processor_id in range(number_of_processers):
            for stage in range(1, number_of_stages + 1):
                taskgroup.create_task(
                    processor(
                        stage,
                        processor_id,
                        controls[stage - 1],
                        controls[stage],
                    )
                )
        # schedule consumers
        for consumer_id in range(number_of_consumers):
            taskgroup.create_task(
                sink(
                    number_of_stages + 1,
                    consumer_id,
                    controls[number_of_stages],
                )
            )


def main():
    asyncio.run(run(32))


if __name__ == '__main__':
    import os

    os.system('clear')
    main()
