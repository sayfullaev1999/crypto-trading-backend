from fastapi import APIRouter, Depends, status

from auth.dependencies import get_auth_service
from auth.schemas import (
    UserRegisterRequest,
    UserResponse,
    TokenResponse,
    UserLoginRequest,
    RefreshTokenRequest,
    LogoutRequest
)
from auth.services.auth import AuthService

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.post(
    path="/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
        data: UserRegisterRequest,
        auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return await auth_service.register(data)


@router.post(
    path="/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
        data: UserLoginRequest,
        auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.login(data)


@router.post(
    path="/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def refresh(
    data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.refresh(data.refresh_token)


@router.post(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    data: LogoutRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    await auth_service.logout(data.refresh_token)
