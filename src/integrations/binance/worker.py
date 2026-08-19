from typing import Any

from integrations.binance.client import BinanceClient
from integrations.binance.services.mapping_service import BinanceMappingService
from integrations.binance.services.price_service import BinancePriceService


class BinanceWorker:
    def __init__(
        self,
        client: BinanceClient,
        mapping_service: BinanceMappingService,
        price_service: BinancePriceService,
    ):
        self.client = client
        self.mapping_service = mapping_service
        self.price_service = price_service

    async def run(self):
        mappings = await self.mapping_service.get_active_mappings()
        markets = [mapping.ticker for mapping in mappings]
        await self.client.create_stream(markets, self.process_message)

    async def process_message(self, data: dict[str, Any]) -> None:
        await self.price_service.save_price_from_book_ticker(data)
