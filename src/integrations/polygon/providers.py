from dishka import Provider, provide, Scope
from redis.asyncio import Redis

from infrastructure.database.database import Database
from integrations.polygon.client import PolygonWebSocketClient
from integrations.polygon.services.mapping_service import PolygonMappingService
from integrations.polygon.services.price_service import PolygonPriceService
from integrations.polygon.worker import PolygonWorker


class PolygonProvider(Provider):
    @provide(scope=Scope.APP)
    def polygon_mapping_service(self, database: Database) -> PolygonMappingService:
        return PolygonMappingService(database)

    @provide(scope=Scope.APP)
    def polygon_price_service(self, redis: Redis) -> PolygonPriceService:
        return PolygonPriceService(redis)

    @provide(scope=Scope.APP)
    def polygon_ws_client(self) -> PolygonWebSocketClient:
        return PolygonWebSocketClient()

    @provide(scope=Scope.APP)
    def polygon_worker(
        self,
        client: PolygonWebSocketClient,
        mapping_service: PolygonMappingService,
        price_service: PolygonPriceService,
    ) -> PolygonWorker:
        return PolygonWorker(client, mapping_service, price_service)
