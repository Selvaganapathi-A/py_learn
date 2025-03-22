import asyncio
import typing


async def run_sequence(*functions: typing.Awaitable[typing.Any]):
    data = []
    for function in functions:
        data.append(await function)
    return data


async def run_parallel(*functions: typing.Awaitable[typing.Any]):
    return await asyncio.gather(*functions)


async def do_thing(message: str):
    await asyncio.sleep(1)
    print(message)
    return len(message)


async def main():
    d = await run_parallel(
        run_sequence(
            do_thing("Turn on TV."),
            do_thing("Mute TV"),
            do_thing("Set volume to 1."),
        ),
        do_thing("Turn on Light."),
        run_sequence(
            do_thing("Turn on AC."),
            do_thing("Set Temperature to 25 deg."),
        ),
        run_sequence(
            do_thing("Flush Toilet."),
            do_thing("Do your Business."),
            do_thing("Flush."),
            do_thing("Flush Again."),
            do_thing("Clean Toilet."),
        ),
    )
    print(d)


if __name__ == "__main__":
    asyncio.run(main())
