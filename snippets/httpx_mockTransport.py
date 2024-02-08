import asyncio


from httpx import Response
from httpx._models import Request


import httpx


class MockHandler(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request: Request) -> Response:
        print(request.headers)
        print(request.url)
        print(request.method)
        print()
        return Response(200, headers=request.headers, text="ok")


async def main():
    mounts: dict[str, MockHandler] = {"http://": MockHandler()}
    client = httpx.AsyncClient(mounts=mounts)
    get_response: Response = await client.get("http://localhost:9000/data")
    print(get_response.encoding)
    print(get_response.content)
    response: tuple[Response, ...] = await asyncio.gather(
        client.post(
            "http://localhost:9000/ds",
            data={
                "hi": b"server",
            },
        ),
        client.post(
            "http://localhost:9000/ds",
            data={
                "hi": b"server",
            },
        ),
        client.post(
            "http://localhost:9000/ds",
            data={
                "hi": b"server",
            },
        ),
        client.post(
            "http://localhost:9000/ds",
            data={
                "hi": b"server",
            },
        ),
        client.post(
            "http://localhost:9000/ds",
            data={
                "hi": b"server",
            },
        ),
        return_exceptions=False,
    )

    print(response)

    pass


if __name__ == "__main__":
    asyncio.run(main())
    print()
    pass
