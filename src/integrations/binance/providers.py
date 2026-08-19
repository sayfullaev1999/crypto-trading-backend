from aioredis import Redis
from dishka import Provider, provide, Scope

from infrastructure.database.database import Database
from integrations.binance.client import BinanceClient
from integrations.binance.services.mapping_service import BinanceMappingService
from integrations.binance.services.price_service import BinancePriceService
from integrations.binance.worker import BinanceWorker


class BinanceProvider(Provider):
    @provide(scope=Scope.APP)
    def binance_mapping_service(self, database: Database) -> BinanceMappingService:
        return BinanceMappingService(database)

    @provide(scope=Scope.APP)
    def binance_price_service(self, redis: Redis) -> BinancePriceService:
        return BinancePriceService(redis)

    @provide(scope=Scope.APP)
    def client(self) -> BinanceClient:
        return BinanceClient()

    @provide(scope=Scope.APP)
    def binance_worker(
        self,
        client: BinanceClient,
        mapping_service: BinanceMappingService,
        price_service: BinancePriceService,
    ) -> BinanceWorker:
        return BinanceWorker(
            client=client,
            mapping_service=mapping_service,
            price_service=price_service
        )
