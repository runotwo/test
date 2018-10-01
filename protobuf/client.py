import asyncio
import aiohttp
import ujson
import datetime
from sys import getsizeof
import helloworld_pb2


def get_dict(size):
    i = 0
    res = {}
    while getsizeof(res) < size:
        res['elem_{}'.format(i)] = 'abcd' * 8
        i += 1
    return res


data = {'method': [], 'size': [], 'rps': []}
sizes = [1024, 10240, 102400, 1048576, 10485760]


async def fetch(loop, id, name):
    async with aiohttp.ClientSession(loop=loop, json_serialize=ujson.dumps) as session:
        data = helloworld_pb2.HelloRequest(name=name)
        data = data.SerializeToString()
        r = await session.post('http://130.193.48.105:8080', data=data)
        d = await r.read()


loop = asyncio.get_event_loop()
for key in sizes:
    request_data = get_dict(key)
    for i in range(30):
        n = datetime.datetime.now()
        loop.run_until_complete(asyncio.wait([fetch(loop, i, 'q'*key) for i in range(200)]))
        data['rps'].append(200 / (datetime.datetime.now() - n).total_seconds())
        data['size'].append(key)
        data['method'].append('protobuf')
        print(i, sep='')
ujson.dump(data, open('protobuf.json', 'w'))
loop.close()
