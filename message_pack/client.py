import asyncio
import datetime
import ujson
from sys import getsizeof

import aiohttp
import umsgpack


def get_dict(size):
    i = 0
    res = {}
    while getsizeof(res) < size:
        res['elem_{}'.format(i)] = 'abcd' * 8
        i += 1
    return res


data = {'method': [], 'size': [], 'rps': []}
sizes = [1024, 10240, 102400]


async def fetch(loop, id, request_data):
    async with aiohttp.ClientSession(loop=loop) as session:
        request_data['id'] = id
        data = umsgpack.packb(request_data)
        r = await session.post('http://130.193.48.105:8080', data=data)
        q = await r.read()


loop = asyncio.get_event_loop()
for key in sizes:
    request_data = get_dict(key)
    for i in range(30):
        n = datetime.datetime.now()
        loop.run_until_complete(asyncio.wait([fetch(loop, i, request_data) for i in range(200)]))
        data['rps'].append(200 / (datetime.datetime.now() - n).total_seconds())
        data['size'].append(key)
        data['method'].append('message_pack')
        print(i, sep='')
ujson.dump(data, open('message_pack.json', 'w'))
loop.close()
