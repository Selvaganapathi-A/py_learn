import asyncio
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Stop:
    """Sentinel used to signal shutdown."""


async def producer(
    out: asyncio.Queue[int],
    shutdown: asyncio.Event,
) -> None:
    try:
        for i in range(1, 100):
            if shutdown.is_set():
                return

            await asyncio.sleep(0.2)

            # simulate catastrophic failure
            if i == 17:
                raise RuntimeError("DATABASE CORRUPTION")

            await out.put(i)
            print(f"[PRODUCER] produced {i}")

    except Exception as exc:
        print(f"[PRODUCER] CRITICAL: {exc}")
        shutdown.set()  # 🔥 global stop signal


async def stage(
    name: str,
    worker_id: int,
    inp: asyncio.Queue,
    out: asyncio.Queue,
    shutdown: asyncio.Event,
) -> None:
    while True:
        # Stop immediately if no work has started
        if shutdown.is_set() and inp.empty():
            return

        try:
            item = await asyncio.wait_for(inp.get(), timeout=0.2)
        except TimeoutError:
            continue

        try:
            await asyncio.sleep(2)  # simulate processing
            print(f"[{name}-{worker_id}] processed {item}")

            if not shutdown.is_set():
                await out.put(item)

        finally:
            inp.task_done()

        # Stop AFTER finishing this item
        if shutdown.is_set():
            return


async def sink(
    worker_id: int,
    inp: asyncio.Queue,
    shutdown: asyncio.Event,
) -> None:
    while True:
        if shutdown.is_set() and inp.empty():
            return

        try:
            item = await asyncio.wait_for(inp.get(), timeout=0.2)
        except TimeoutError:
            continue

        try:
            await asyncio.sleep(0.8)
            print(f"[SINK-{worker_id}] consumed {item}")

        finally:
            inp.task_done()

        if shutdown.is_set():
            return


async def run() -> None:
    stages = 1
    workers_per_stage = 8
    sink_workers = 4

    shutdown_event = asyncio.Event()

    queues = [asyncio.Queue(maxsize=10) for _ in range(stages + 1)]

    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            producer(
                queues[0],
                shutdown_event,
            )
        )

        for stage_idx in range(stages):
            for w in range(workers_per_stage):
                tg.create_task(
                    stage(
                        f"STAGE-{stage_idx + 1}",
                        w,
                        queues[stage_idx],
                        queues[stage_idx + 1],
                        shutdown=shutdown_event,
                    )
                )

        for w in range(sink_workers):
            tg.create_task(sink(w, queues[-1], shutdown=shutdown_event))


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
