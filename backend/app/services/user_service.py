from uuid import UUID
from datetime import datetime
from typing import Optional, Sequence, Any
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService
from app.core.security import get_password_hash, get_password_verify
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InvalidCredentialsError,
)
from app.repositories.user_repository import UserRepository


class UserService(BaseService[UserRepository]):
    """
    Service layer for User operations.

    All business logic related to users should go here:
    - Creating/updating/deleting users
    - Authentication
    - Permission checks (if needed)
    """

    def __init__(self, user_repo: UserRepository):
        super().__init__(user_repo)

    async def login_user(self, username: str | None ,email: str | None , password: str, db: AsyncSession) -> Optional[User]:
        """Authenticate a user with username and password."""
        
        if username is not None:
            user = await self.repository.get_by_username(db, username)
        elif email is not None:
            user = await self.repository.get_by_email(db, email)
        else:
            raise InvalidCredentialsError()

        if not user:
            raise InvalidCredentialsError()
        if not get_password_verify(password, user.hashed_password):
            raise InvalidCredentialsError()
        return user

    async def create_user(self, user_in: UserCreate, db: AsyncSession) -> User:
        """Create a new user."""
        # Check if username or email already exists
        existing_user = await self.repository.get_by_username_or_email(db,user_in.username, user_in.email)
        if existing_user:
            raise EntityAlreadyExistsError("User", "username/email", f"{user_in.username}/{user_in.email}")

        # Hash the password
        hashed_password = get_password_hash(user_in.password)

        data = user_in.model_dump()
        raw_password = data.pop("password")
        
        data["hashed_password"] = hashed_password
        
        return await self.repository.create(db, data)

    async def get_all_user(self, db: AsyncSession) -> Sequence[User] :
        """Get all users."""
        result = await self.repository.get_all(db)
        return result

    async def get_user_by_id(self, user_id: UUID, db: AsyncSession) -> Optional[User]:
        """Get a user by ID."""
        result = await self.repository.get_by_id(db, user_id)
        return result

   

    async def authenticate_user(self, username: str, password: str, db: AsyncSession) -> Optional[User]:
        """Authenticate a user with username and password."""
        user = await self.repository.get_by_username(db, username)
        
        if not user:
            raise InvalidCredentialsError()
        if not get_password_verify(password, user.hashed_password):
            raise InvalidCredentialsError()
        return user

    async def update_user(self, user_id: UUID, user_in: UserUpdate, db: AsyncSession) -> Optional[User]:
        """Update a user's information."""
        # Check if user exists
        existing_user = await self.repository.get_by_id(db, user_id)
        if not existing_user:
            raise EntityNotFoundError("User", user_id)

        # Check if another user already has the same username or email
        result = await self.repository.get_by_username_or_email(db, user_in.username, user_in.email)

        if result and result.id != user_id:
            raise EntityAlreadyExistsError("User", "username/email", f"{user_in.username}/{user_in.email}")

        # Update fields
        update_data = user_in.model_dump(exclude_unset=True)
        
        if 'password' in update_data and update_data['password'] is not None:
            update_data['hashed_password'] = get_password_hash(update_data.pop('password'))

        
        return await self.repository.update(db, user_id, update_data)

    async def delete_user(self, user_id: UUID, db: AsyncSession) -> bool:
        """Delete a user."""
        user = await self.repository.get_by_id(db, user_id)
        if not user:
            return False
        return await self.repository.delete(db, user_id)

    # async def get_users_paginated(
    #     self,
    #     skip: int = 0,
    #     limit: int = 100,
    # ) -> Sequence[User]:
    #     """Get a paginated list of users."""
    #     result = await self.db.execute(
    #         select(User).offset(skip).limit(limit)
    #     )
    #     return result.scalars().all()