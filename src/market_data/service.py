from fastapi import WebSocket

from market_data.managers import ConnectionManager


class MarketDataService:
    def __init__(self, connection_manager: ConnectionManager) -> None:
        self.connection_manager = connection_manager

    async def connect(self, websocket: WebSocket) -> None:
        await self.connection_manager.connect(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.connection_manager.disconnect(websocket)

    async def subscribe(self, websocket: WebSocket, symbols: list[str]):
        await self.connection_manager.send(
            websocket,
            {
                "type": "subscribed",
                "symbols": symbols
            }
        )
