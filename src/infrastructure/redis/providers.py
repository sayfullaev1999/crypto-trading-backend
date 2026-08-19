from typing import AsyncIterable

from redis.asyncio import Redis

from dishka import provide, Scope, Provider

from core.settings import settings


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def redis(self) -> AsyncIterable[Redis]:
        redis = Redis.from_url(
            str(settings.REDIS_DSN),
            decode_responses=True,
        )
        yield redis
        await redis.close()
