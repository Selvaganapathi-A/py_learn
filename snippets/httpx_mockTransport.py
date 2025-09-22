import asyncio
from pprint import pprint

import httpx
from httpx import Response
from httpx._models import Request


class MockHandler(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request: Request) -> Response:
        print(request.url)
        print(request.method)
        pprint({**request.headers})
        return Response(200, headers=request.headers, text='ok')


async def main():
    mounts: dict[str, MockHandler] = {'http://': MockHandler()}
    client = httpx.AsyncClient(mounts=mounts)
    get_response: Response = await client.get('http://localhost:9000/data')
    print(get_response.encoding)
    print(get_response.content)
    responses: tuple[Response, ...] = await asyncio.gather(
        client.post(
            'http://localhost:9000/ds',
            data={
                'hi': b'server',
            },
        ),
        client.post(
            'http://localhost:9000/ds',
            data={
                'hi': b'server',
            },
        ),
        client.post(
            'http://localhost:9000/ds',
            data={
                'hi': b'server',
            },
        ),
        client.post(
            'http://localhost:9000/ds',
            data={
                'hi': b'server',
            },
        ),
        client.post(
            'http://localhost:9000/ds',
            data={
                'hi': b'server',
            },
        ),
        return_exceptions=False,
    )
    for response in responses:
        print(response.url)
        print(response.status_code)
        print(response.content)


if __name__ == '__main__':
    asyncio.run(main())
