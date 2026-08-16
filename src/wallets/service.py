import json
from uuid import UUID

from core.settings import settings
from wallets.managers import WalletManager
from wallets.models import Wallet
from wallets.repository import WalletRepository

from eth_account.account import Account


class WalletService:
    def __init__(
        self,
        wallet_repository: WalletRepository,
        wallet_manager: WalletManager
    ):
        self.wallet_repository = wallet_repository
        self.wallet_manager = wallet_manager

    async def create_wallet(self, user_id: UUID) -> Wallet:
        account = Account.create()

        encrypted = self.wallet_manager.encrypt_private_key(
            private_key=account.key,
            password=settings.WALLET_ENCRYPTION_PASSWORD
        )

        encrypted_private_key = json.dumps(encrypted)

        return await self.wallet_repository.create(
            address=account.address,
            user_id=user_id,
            encrypted_private_key=encrypted_private_key
        )
