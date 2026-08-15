from pwdlib import PasswordHash

from auth.exceptions import InvalidCredentialsError
from auth.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse
from auth.services.token import TokenService
from users.exceptions import UserAlreadyExistsError
from users.repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository, token_service: TokenService):
        self.user_repository = user_repository
        self.token_service = token_service
        self.password_hasher = PasswordHash.recommended()

    async def register(self, data: UserRegisterRequest):
        existing_user = await self.user_repository.get_by_email(data.email)

        if existing_user:
            raise UserAlreadyExistsError

        return await self.user_repository.create(
            email=data.email,
            password_hash=self.password_hasher.hash(data.password),
        )

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
