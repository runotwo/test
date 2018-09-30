from aiohttp import web
import ujson


async def handle(request):
    data = await request.json()
    return web.json_response({'status': 'ok', 'id': data['id']})


app = web.Application()
app.add_routes([web.post("/", handle), ])

web.run_app(app)