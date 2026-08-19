import json
import logging

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class BinancePriceService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_price_from_book_ticker(self, data: dict[str, str | int]):
        try:
            symbol = data.get("symbol")
            if not symbol:
                return

            cache_data = {
                "bid": float(data["best_bid_price"]),
                "ask": float(data["best_ask_price"]),
                "mid": (float(data["best_bid_price"]) + float(data["best_ask_price"])) / 2,
                "timestamp": data["order_book_update_id"]
            }
            await self.redis.set(f"price:{symbol}", json.dumps(cache_data))
        except KeyError as exp:
            logger.exception("Failed to save price data from book ticker, %s", exp)
