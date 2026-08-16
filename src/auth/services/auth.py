from pwdlib import PasswordHash

from auth.exceptions import InvalidCredentialsError
from auth.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse
from auth.services.token import TokenService
from infrastructure.database.uow import UnitOfWork
from users.exceptions import UserAlreadyExistsError
from users.repository import UserRepository
from wallets.service import WalletService


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        uow: UnitOfWork,
        token_service: TokenService,
        wallet_service: WalletService,
    ):
        self.user_repository = user_repository
        self.uow = uow
        self.token_service = token_service
        self.wallet_service = wallet_service
        self.password_hasher = PasswordHash.recommended()

    async def register(self, data: UserRegisterRequest):
        existing_user = await self.user_repository.get_by_email(data.email)

        if existing_user:
            raise UserAlreadyExistsError

        async with self.uow:
            user = await self.user_repository.create(
                email=data.email,
                password_hash=self.password_hasher.hash(data.password),
            )
            _ = await self.wallet_service.create_wallet(user.id)

        return user

    async def login(self, data: UserLoginRequest):
        user = await self.user_repository.get_by_email(data.email)

        if not user:
            raise InvalidCredentialsError

        if not self.password_hasher.verify(
            password=data.password,
            hashed_password=user.password_hash
        ):
            raise InvalidCredentialsError

        access_token, refresh_token = await self.token_service.create_token_pair(user_id=user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        access_token, new_refresh_token = await self.token_service.refresh(refresh_token)
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

    async def logout(self, refresh_token: str) -> None:
        await self.token_service.revoke(refresh_token)
