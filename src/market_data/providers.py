from dishka import Provider, provide, Scope

from market_data.managers import ConnectionManager
from market_data.service import MarketDataService


class MarketDataProvider(Provider):
    @provide(scope=Scope.APP)
    def connection_manager(self) -> ConnectionManager:
        return ConnectionManager()

    @provide(scope=Scope.REQUEST)
    def market_data_service(self, connection_manager: ConnectionManager) -> MarketDataService:
        return MarketDataService(
            connection_manager=connection_manager
        )
