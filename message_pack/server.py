import umsgpack
from aiohttp import web


async def handle(request):
    name = request.match_info.get("name", "Anonymous")
    data = await request.read()
    data = umsgpack.unpackb(data)
    text = "Hello, " + name
    return web.Response(body=umsgpack.packb({'name': name, 'text': text, 'id': data['id']}))


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([web.post("/", handle)])
    web.run_app(app, port=8888)
