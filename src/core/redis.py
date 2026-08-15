from aioredis import Redis


class RedisClient:
    def __init__(self, redis_url: str) -> None:
        self.client = Redis.from_url(
            redis_url,
            decode_responses=True,
        )

    async def close(self) -> None:
        await self.client.close()
