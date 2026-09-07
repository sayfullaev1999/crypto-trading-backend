from polygon.websocket import WebSocketMessage
from redis.asyncio import Redis


class PolygonPriceService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_price(self, messages: list[WebSocketMessage]) -> None:
        pass

