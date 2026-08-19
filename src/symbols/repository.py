from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from symbols.models import Symbol


class SymbolRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_symbols(self):
        result = await self.session.execute(
            select(Symbol).where(Symbol.is_active.is_(True))
        )
        return result.scalars().all()
