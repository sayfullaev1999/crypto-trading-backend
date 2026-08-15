from fastapi import Request, status
from fastapi.responses import JSONResponse

from auth.exceptions import InvalidCredentialsError, InvalidTokenError
from users.exceptions import UserAlreadyExistsError


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid credentials"},
    )


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "User already exists"},
    )


async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid token"},
    )

