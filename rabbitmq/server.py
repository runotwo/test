import asyncio
from aio_pika import connect, IncomingMessage
from datetime import datetime
import ujson




async def ww():
    data = {'method': [], 'size': [], 'rps': []}
    p = {'c_pack': None, 'c_time': None}

    async def wrapped(message: IncomingMessage):
        body = ujson.loads(message.body)
        del body['q']
        body['time'] = datetime.now()
        if not p['c_pack']:
            p['c_pack'] = body['pack']
            p['c_time'] = body['time']
        if p['c_pack'] != body['pack']:
            data['rps'].append(200 / (datetime.now() - p['c_time']).total_seconds())
            data['size'].append(body['size'])
            data['method'].append('mq')
            p['c_pack'] = None
            p['c_time'] = None
        print(body)
    return wrapped



async def main(loop):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    # Declaring queue
    queue = await channel.declare_queue('hello')

    # Start listening the queue with name 'hello'
    await queue.consume(await ww(), no_ack=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    print(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()
