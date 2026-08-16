from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from wallets.models import Wallet


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, address: str, user_id: UUID, encrypted_private_key: str):
        wallet = Wallet(
            address=address,
            user_id=user_id,
            encrypted_private_key=encrypted_private_key
        )

        self.session.add(wallet)
        await self.session.flush()

        return wallet
