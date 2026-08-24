from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.pagination import PaginationParams, paginate, PaginationResult

from symbols.models import Symbol


class SymbolRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_symbols(
        self,
        pagination: PaginationParams,
        is_active: bool = True,
    ) -> PaginationResult[Symbol]:
        query = select(Symbol).where(Symbol.is_active.is_(is_active))

        return await paginate(self.session, query, pagination)
