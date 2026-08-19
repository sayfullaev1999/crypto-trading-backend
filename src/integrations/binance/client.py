import asyncio
from collections.abc import Callable, Awaitable
from typing import Any

from unicorn_binance_websocket_api import BinanceWebSocketApiManager


MessageHandler = Callable[[dict[str, Any]], Awaitable[None]]


class BinanceClient:
    CHANNELS = ['bookTicker']

    def __init__(self):
        self.websocket_manager = BinanceWebSocketApiManager(
            output_default="UnicornFy",
        )
        self._process_message: MessageHandler | None = None

    async def create_stream(
        self,
        markets: list[str],
        process_message: MessageHandler
    ) -> None:
        self._process_message = process_message

        self.websocket_manager.create_stream(
            channels=self.CHANNELS,
            markets=markets,
            process_asyncio_queue=self._process_asyncio_queue,
        )

        while not self.websocket_manager.is_manager_stopping():
            await asyncio.sleep(1)

    async def _process_asyncio_queue(self, stream_id: str) -> None:
        while self.websocket_manager.is_stop_request(stream_id) is False:
            data = await self.websocket_manager.get_stream_data_from_asyncio_queue(stream_id)

            await self._process_message(data)

            self.websocket_manager.asyncio_queue_task_done(stream_id)
