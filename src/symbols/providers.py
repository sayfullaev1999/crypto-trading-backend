from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from symbols.repository import SymbolRepository


class SymbolProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def symbol_repository(self, session: AsyncSession) -> SymbolRepository:
        return SymbolRepository(session)
