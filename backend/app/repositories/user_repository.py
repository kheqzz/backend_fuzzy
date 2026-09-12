from typing import Generic, TypeVar, TYPE_CHECKING
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

if TYPE_CHECKING:
    from uuid import UUID



class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repository for User model."""

    def __init__(self):
        super().__init__(User)
        
    # Add custom query methods if needed
    async def get_by_email(self, db, email: str) -> User | None:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_by_username(self, db, username: str) -> User | None:
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()