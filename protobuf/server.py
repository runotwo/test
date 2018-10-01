import asyncio

from aiohttp import web
from protobuf import helloworld_pb2


async def handle(request):
    data = await request.read()
    name = helloworld_pb2.HelloRequest.FromString(data).name
    text = "Hello, " + name
    return web.Response(body=data)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.post("/", handle)])
    web.run_app(app)
