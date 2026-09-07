from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.polygon.models import PolygonMapping
from symbols.models import Symbol, SymbolType


class PolygonMappingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_mappings_by_symbol_type(self, symbol_type: SymbolType) -> list[PolygonMapping]:
        result = await self.session.execute(
            select(PolygonMapping)
            .join(
                Symbol,
                Symbol.id == PolygonMapping.symbol_id
            )
            .where(Symbol.is_active.is_(True), Symbol.type == symbol_type)
        )
        return list(result.scalars().all())
