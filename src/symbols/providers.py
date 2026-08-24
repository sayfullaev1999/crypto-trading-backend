from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from symbols.repository import SymbolRepository
from symbols.service import SymbolService


class SymbolProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def symbol_repository(self, session: AsyncSession) -> SymbolRepository:
        return SymbolRepository(session)

    @provide(scope=Scope.REQUEST)
    def symbol_service(self, symbol_repository: SymbolRepository) -> SymbolService:
        return SymbolService(
            symbol_repository=symbol_repository,
        )
