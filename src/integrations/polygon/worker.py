from polygon.websocket import WebSocketMessage

from symbols.enums import SymbolType
from .client import PolygonWebSocketClient
from .services.mapping_service import PolygonMappingService
from .services.price_service import PolygonPriceService


class PolygonWorker:
    def __init__(
        self,
        client: PolygonWebSocketClient,
        mapping_service: PolygonMappingService,
        price_service: PolygonPriceService,
    ):
        self.client = client
        self.mapping_service = mapping_service
        self.price_service = price_service

    async def run(self):
        crypto_mappings = await self.mapping_service.get_mappings_by_symbol_type(SymbolType.CRYPTO)
        forex_mappings = await self.mapping_service.get_mappings_by_symbol_type(SymbolType.FOREX)

        await self.client.connect(
            crypto_subscriptions=[mapping.ws_ticker for mapping in crypto_mappings],
            forex_subscriptions=[mapping.ws_ticker for mapping in forex_mappings],
            handler=self.process_message
        )

    async def process_message(self, messages: list[WebSocketMessage]):
        await self.price_service.save_price(messages)
