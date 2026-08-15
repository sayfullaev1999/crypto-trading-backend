from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.exceptions import InvalidCredentialsError, InvalidTokenError
from core.exception_handlers import (
    invalid_credentials_handler,
    user_already_exists_handler,
    invalid_token_handler
)
from core.settings import settings
from core.container import container
from auth import router as auth_router
from users.exceptions import UserAlreadyExistsError


@asynccontextmanager
async def lifespan(app_: FastAPI):
    database = container.database()
    redis_client = container.redis_client()

    yield

    await database.close()
    await redis_client.close()


def register_routers(app_: FastAPI):
    app_.include_router(auth_router.router)


def register_exception_handlers(app_: FastAPI):
    app_.add_exception_handler(
        InvalidCredentialsError,
        invalid_credentials_handler,
    )

    app_.add_exception_handler(
        UserAlreadyExistsError,
        user_already_exists_handler,
    )
    app_.add_exception_handler(
        InvalidTokenError,
        invalid_token_handler,
    )


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

register_routers(app)
register_exception_handlers(app)
