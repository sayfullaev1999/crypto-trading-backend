from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.container import container


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    database = container.database()

    async with database.session_factory() as session:
        yield session
