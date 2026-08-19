from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.binance.models import BinanceMapping
from symbols.models import Symbol


class BinanceMappingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_mappings(self) -> list[BinanceMapping]:
        result = await self.session.execute(
            select(BinanceMapping)
            .join(
                Symbol,
                Symbol.id == BinanceMapping.symbol_id
            )
            .where(Symbol.is_active.is_(True))
        )
        return list(result.scalars().all())
