from typing import AsyncIterable

from redis.asyncio import Redis, Sentinel

from dishka import provide, Scope, Provider

from core.settings import settings


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def redis(self) -> AsyncIterable[Redis]:
        sentinel_hosts = [
            (host, int(port))
            for item in settings.REDIS_SENTINEL_HOSTS.split(",")
            for host, port in [item.split(":")]
        ]
        sentinel = Sentinel(
            sentinel_hosts,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )
        redis = sentinel.master_for(
            service_name=settings.REDIS_SENTINEL_MASTER_NAME,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )
        try:
            yield redis
        finally:
            await redis.aclose()
            await sentinel.aclose()
