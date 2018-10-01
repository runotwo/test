import asyncio
from aio_pika import connect, Message
import ujson
import datetime


async def send(id, data, channel):
    data['id'] = id
    await channel.default_exchange.publish(
        Message(bytes(ujson.dumps(data), 'utf-8')),
        routing_key='hello',
    )

sizes = [1024, 10240, 102400]


async def main(loop):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()
    qq = 30
    # Sending the message
    for key in sizes:
        now = datetime.datetime.now()
        request_data = {'q': 'a'*key, 'size': key}
        if key == 102400:
            qq = 31
        for i in range(qq):
            request_data['pack'] = i
            await asyncio.wait([send(k, request_data, channel) for k in range(200)])

    await connection.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))