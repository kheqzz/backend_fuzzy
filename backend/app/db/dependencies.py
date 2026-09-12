from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_factory
from collections.abc import AsyncGenerator


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
