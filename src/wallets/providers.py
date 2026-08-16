from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from wallets.managers import WalletManager
from wallets.repository import WalletRepository
from wallets.service import WalletService


class WalletProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def wallet_repository(self, session: AsyncSession) -> WalletRepository:
        return WalletRepository(session)

    @provide(scope=Scope.REQUEST)
    def wallet_service(
        self,
        wallet_repository: WalletRepository,
        wallet_manager: WalletManager
    ) -> WalletService:
        return WalletService(
            wallet_repository=wallet_repository,
            wallet_manager=wallet_manager
        )

    @provide(scope=Scope.APP)
    def wallet_manager(self) -> WalletManager:
        return WalletManager()
