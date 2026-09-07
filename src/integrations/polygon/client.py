import asyncio
from typing import Callable, Awaitable

from polygon import WebSocketClient
from polygon.websocket import WebSocketMessage
from polygon.websocket.models import Market


MessageHandler = Callable[[list[WebSocketMessage]], Awaitable[None]]


class PolygonWebSocketClient:
    def __init__(self):
        self.connections: dict[Market, WebSocketClient] = {}

    async def _connect(self, market: Market, subscriptions: list[str], handler: MessageHandler):
        client = WebSocketClient(
            subscriptions=subscriptions,
            api_key="",
            market=market,
        )

        self.connections[market] = client

        await client.connect(handler)

    async def crypto_connect(self, subscriptions: list[str], handler: MessageHandler):
        await self._connect(
            subscriptions=subscriptions,
            market=Market.Crypto,
            handler=handler
        )

    async def forex_connect(self, subscriptions: list[str], handler: MessageHandler):
        await self._connect(
            subscriptions=subscriptions,
            market=Market.Forex,
            handler=handler
        )

    async def connect(
        self,
        crypto_subscriptions: list[str],
        forex_subscriptions: list[str],
        handler: MessageHandler,
    ):
        await asyncio.gather(
            self.crypto_connect(
                subscriptions=crypto_subscriptions,
                handler=handler,
            ),
            self.forex_connect(
                subscriptions=forex_subscriptions,
                handler=handler,
            ),
        )

    async def close(self) -> None:
        for client in self.connections.values():
            await client.close()
        self.connections.clear()
