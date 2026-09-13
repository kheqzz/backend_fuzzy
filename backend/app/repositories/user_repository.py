from typing import Generic, TypeVar, TYPE_CHECKING
from sqlalchemy import select, or_
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from uuid import UUID
# if TYPE_CHECKING:
#     from uuid import UUID



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

    async def get_by_username_or_email(self, db, username: str | None = None, email: str | None = None) -> User | None:

        if not username and not email:
            return None  # Return None if both username and email are None

        conditions = []
        if username:
            conditions.append(User.username == username)
        if email:
            conditions.append(User.email == email)
        result = await db.execute(
            select(User).where(
                or_(*conditions)
            )
        )
        return result.scalars().first()

    async def get_by_id(self, db, user_id: UUID) -> User | None:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()