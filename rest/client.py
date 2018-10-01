import asyncio
import datetime

import aiohttp
import ujson


async def fetch(loop, data):
    async with aiohttp.ClientSession(loop=loop, json_serialize=ujson.dumps) as session:
        async with session.post('http://130.193.48.105:8080', json=data) as resp:
            data = await resp.json()


res={'size': [], 'time': [], 'method': []}
sizes = [1024, 10240, 102400, 1048576, 10485760]


async def go(loop):
    for size in sizes:
        data = {'name': 'a'*size, 'id': 1}
        for i in range(30):
            time = datetime.datetime.now()
            await asyncio.wait([fetch(loop, data) for x in range(100)])
            res['time'].append(100/(datetime.datetime.now()-time).total_seconds())
            res['size'].append(size)
            res['method'].append('ujson')
            print(size, i)

loop = asyncio.get_event_loop()
loop.run_until_complete(go(loop))
loop.close()
ujson.dump(res, open('res.json', 'w'))
