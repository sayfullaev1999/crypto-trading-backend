from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.container import container
from database.dependencies import get_db_session
from users.repository import UserRepository


def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return container.user_repository(
        session=session,
    )
