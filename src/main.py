from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from auth.exceptions import InvalidCredentialsError, InvalidTokenError, UnAuthorizedError
from core.containers import app_container
from core.exception_handlers import (
    invalid_credentials_handler,
    user_already_exists_handler,
    invalid_token_handler, unauthorized_user_handler
)
from core.settings import settings
from auth import router as auth_router
from symbols import router as symbols_router
from users.exceptions import UserAlreadyExistsError


def register_routers(app_: FastAPI):
    app_.include_router(auth_router.router)
    app_.include_router(symbols_router.router)


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
    app_.add_exception_handler(
        UnAuthorizedError,
        unauthorized_user_handler
    )


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

register_routers(app)
register_exception_handlers(app)
setup_dishka(app_container, app)
