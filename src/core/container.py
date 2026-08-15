from dependency_injector import containers, providers

from auth.services.jwt import JWTService
from auth.services.auth import AuthService
from auth.services.token import TokenService
from core.redis import RedisClient
from core.settings import settings
from database.database import Database
from users.repository import UserRepository


class Container(containers.DeclarativeContainer):
    database = providers.Singleton(
        Database, database_url=str(settings.POSTGRES_DSN),
    )
    redis_client = providers.Singleton(
        RedisClient, redis_url=str(settings.REDIS_DSN),
    )

    user_repository = providers.Factory(UserRepository)
    jwt_service = providers.Factory(
        JWTService,
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        access_token_expire_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS,
        refresh_token_expire_seconds=settings.JWT_REFRESH_TOKEN_EXPIRE_SECONDS,

    )
    token_service = providers.Factory(
        TokenService,
        jwt_service=jwt_service,
        redis=redis_client,
    )
    auth_service = providers.Factory(
        AuthService,
        token_service=token_service,
    )


container = Container()
