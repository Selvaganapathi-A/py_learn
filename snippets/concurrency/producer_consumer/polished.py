import asyncio
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar('T')


@dataclass(slots=True)
class Stop:
    """Sentinel used to signal shutdown."""


async def producer(
    out: asyncio.Queue[int],
    count: int,
    workers: int,
) -> None:
    """
    Produce integers and send STOP sentinels.
    """
    for i in range(1, count + 1):
        await asyncio.sleep(0.05)
        await out.put(i)
        print(f'[PRODUCER] produced {i}')

    # Signal downstream workers to stop
    for _ in range(workers):
        await out.put(Stop())


async def stage(
    name: str,
    worker_id: int,
    inp: asyncio.Queue,
    out: asyncio.Queue,
) -> None:
    """
    Generic pipeline stage.
    """
    while True:
        item = await inp.get()
        try:
            if isinstance(item, Stop):
                await out.put(item)
                return

            await asyncio.sleep(0.1)
            print(f'[{name}-{worker_id}] processed {item}')
            await out.put(item)

        finally:
            inp.task_done()


async def sink(
    worker_id: int,
    inp: asyncio.Queue,
) -> None:
    """
    Final consumer.
    """
    while True:
        item = await inp.get()
        try:
            if isinstance(item, Stop):
                return

            await asyncio.sleep(0.15)
            print(f'[SINK-{worker_id}] consumed {item}')

        finally:
            inp.task_done()


async def run() -> None:
    stages = 3
    workers_per_stage = 4
    sink_workers = 3

    queues = [asyncio.Queue(maxsize=10) for _ in range(stages + 1)]

    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            producer(
                queues[0],
                count=30,
                workers=workers_per_stage,
            )
        )

        for stage_idx in range(stages):
            for w in range(workers_per_stage):
                tg.create_task(
                    stage(
                        f'STAGE-{stage_idx + 1}',
                        w,
                        queues[stage_idx],
                        queues[stage_idx + 1],
                    )
                )

        for w in range(sink_workers):
            tg.create_task(sink(w, queues[-1]))


def main() -> None:
    asyncio.run(run())


if __name__ == '__main__':
    main()
