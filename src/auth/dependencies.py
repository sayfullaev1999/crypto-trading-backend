from fastapi import Depends

from auth.services.auth import AuthService
from core.container import container
from users.dependencies import get_user_repository
from users.repository import UserRepository


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return container.auth_service(
        user_repository=user_repository
    )
