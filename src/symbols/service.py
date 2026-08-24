from core.pagination import PaginationParams, PaginationResult
from symbols.models import Symbol
from symbols.repository import SymbolRepository


class SymbolService:
    def __init__(self, symbol_repository: SymbolRepository):
        self.symbol_repository = symbol_repository

    async def get_symbols(
        self,
        pagination: PaginationParams
    ) -> PaginationResult[Symbol]:
        return await self.symbol_repository.get_symbols(
            pagination=pagination,
            is_active=True
        )
