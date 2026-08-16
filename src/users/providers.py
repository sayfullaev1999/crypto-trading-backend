from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from users.repository import UserRepository


class UsersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)
