from uuid import UUID
from datetime import datetime
from typing import Optional, Sequence
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, get_password_verify
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InvalidCredentialsError,
)


class UserService:
    """
    Service layer for User operations.

    All business logic related to users should go here:
    - Creating/updating/deleting users
    - Authentication
    - Permission checks (if needed)
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_in: UserCreate) -> User:
        """Create a new user."""
        # Check if username or email already exists
        existing_user = await self.db.execute(
            select(User).where(
                or_(User.username == user_in.username, User.email == user_in.email)
            )
        )
        if existing_user.fetchone():
            # Determine which field conflicts
            conflict = existing_user.keys()
            if "username" in conflict:
                raise EntityAlreadyExistsError("User", "username", user_in.username)
            else:
                raise EntityAlreadyExistsError("User", "email", user_in.email)

        # Hash the password
        hashed_password = get_password_hash(user_in.password)

        # Create new user instance
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hashed_password,
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_all_user(self) -> Sequence[User] :
        """Get all users."""
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by ID."""
        result = await self.db.get(User, user_id)
        return result

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalars().first()
        if not user:
            raise InvalidCredentialsError()
        if not get_password_verify(password, user.hashed_password):
            raise InvalidCredentialsError()
        return user

    async def update_user(
        self, user_id: UUID, user_in: UserUpdate
    ) -> Optional[User]:
        """Update a user's information."""
        # Check if user exists
        existing_user = await self.get_user_by_id(user_id)
        if not existing_user:
            raise EntityNotFoundError("User", user_id)

        # Check if another user already has the same username or email
        result = await self.db.execute(
            select(User).where(
                or_(User.username == user_in.username, User.email == user_in.email),
                User.id != user_id,
            )
        )

        if result.fetchone():
            conflict = result.keys()
            if "username" in conflict:
                assert user_in.username is not None  # Ensure username is provided 
                raise EntityAlreadyExistsError("User", "username", user_in.username)
            else:
                assert user_in.email is not None
                raise EntityAlreadyExistsError("User", "email", user_in.email)

        # Update fields
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_user, field, value)

        # Hash password if changed
        if hasattr(user_in, "password") and user_in.password is not None:
            existing_user.hashed_password = get_password_hash(user_in.password)

        await self.db.commit()
        await self.db.refresh(existing_user)
        return existing_user

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user."""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def get_users_paginated(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        """Get a paginated list of users."""
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()