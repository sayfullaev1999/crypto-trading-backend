from infrastructure.database.database import Database
from integrations.polygon.models import PolygonMapping
from integrations.polygon.repository import PolygonMappingRepository
from symbols.enums import SymbolType


class PolygonMappingService:
    def __init__(self, database: Database):
        self.database = database

    async def get_mappings_by_symbol_type(self, symbol_type: SymbolType) -> list[PolygonMapping]:
        async with self.database.session_factory() as session:
            repository = PolygonMappingRepository(session)

            return await repository.get_mappings_by_symbol_type(symbol_type)
