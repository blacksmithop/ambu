import aioredis
import asyncio


class Tag:
    def __init__(self):
        self.con = None

    async def connect(self):
        self.con = await aioredis.create_redis_pool(('localhost', 6379))

    async def ping(self):
        print(await self.con.ping())


if __name__ == '__main__':
    test = Tag()
    asyncio.run(test.connect())


