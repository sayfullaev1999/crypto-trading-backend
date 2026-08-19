from infrastructure.database.database import Database
from integrations.binance.models import BinanceMapping
from integrations.binance.repository import BinanceMappingRepository


class BinanceMappingService:
    def __init__(self, database: Database):
        self.database = database

    async def get_active_mappings(self) -> list[BinanceMapping]:
        async with self.database.session_factory() as session:
            repository = BinanceMappingRepository(session)

            return await repository.get_active_mappings()
