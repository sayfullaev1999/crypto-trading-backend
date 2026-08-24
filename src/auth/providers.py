from redis.asyncio import Redis
from dishka import provide, Scope, Provider, from_context
from fastapi import Request

from auth.services.auth import AuthService
from auth.services.jwt import JWTService
from auth.services.token import TokenService
from core.settings import settings
from infrastructure.database.uow import UnitOfWork
from users.models import User
from users.repository import UserRepository
from wallets.service import WalletService


class AuthProvider(Provider):
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
        self,
        request: Request,
        auth_service: AuthService,
    ) -> User:
        authorization = request.headers.get("Authorization")
        return await auth_service.get_user_by_token(authorization)

    @provide(scope=Scope.REQUEST)
    def auth_service(
        self,
        user_repository: UserRepository,
        uow: UnitOfWork,
        token_service: TokenService,
        wallet_service: WalletService,
    ) -> AuthService:
        return AuthService(
            user_repository=user_repository,
            uow=uow,
            token_service=token_service,
            wallet_service=wallet_service,
        )

    @provide(scope=Scope.APP)
    def jwt_service(self) -> JWTService:
        return JWTService(
            secret_key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
            access_token_expire_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
            refresh_token_expire_seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,
        )

    @provide(scope=Scope.APP)
    def token_service(
        self,
        jwt_service: JWTService,
        redis: Redis
    ) -> TokenService:
        return TokenService(
            jwt_service=jwt_service,
            redis=redis
        )
