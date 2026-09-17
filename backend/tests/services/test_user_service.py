"""Test UserService."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from uuid import uuid4
from app.services.user_service import UserService
from app.models.user import User
from app.core.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InvalidCredentialsError,
)
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash


class TestUserService:
    """Tests for UserService."""

    @pytest.fixture
    def service(self):
        return UserService(UserRepository())

    def _mock_db_with_user(self):
        """Create a mock db that simulates db.execute returning a user."""
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.get = AsyncMock()
        return mock_db, mock_result

    @pytest.mark.asyncio
    async def test_create_user_success(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        from app.schemas.user import UserCreate
        user_in = UserCreate(
            username="newuser",
            email="new@test.com",
            full_name="New User",
            password="password123",
        )
        result = await service.create_user(user_in, mock_db)
        assert result.username == "newuser"
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_duplicate_raises(self, service):
        existing = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = existing
        mock_db.execute = AsyncMock(return_value=mock_result)

        from app.schemas.user import UserCreate
        user_in = UserCreate(
            username="test",
            email="test@test.com",
            full_name="Test",
            password="password123",
        )
        with pytest.raises(EntityAlreadyExistsError):
            await service.create_user(user_in, mock_db)

    @pytest.mark.asyncio
    async def test_login_user_success(self, service):
        hashed = get_password_hash("correctpass")
        user = User(
            username="testuser",
            email="test@test.com",
            full_name="Test",
            hashed_password=hashed,
        )
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await service.login_user(
            username="testuser", email=None, password="correctpass", db=mock_db
        )
        assert result == user

    @pytest.mark.asyncio
    async def test_login_user_wrong_password(self, service):
        hashed = get_password_hash("correctpass")
        user = User(
            username="testuser",
            email="test@test.com",
            full_name="Test",
            hashed_password=hashed,
        )
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(InvalidCredentialsError):
            await service.login_user(
                username="testuser", email=None, password="wrongpass", db=mock_db
            )

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(InvalidCredentialsError):
            await service.login_user(
                username="nonexistent", email=None, password="pass", db=mock_db
            )

    @pytest.mark.asyncio
    async def test_login_user_with_email(self, service):
        hashed = get_password_hash("pass")
        user = User(
            username="test",
            email="test@test.com",
            full_name="Test",
            hashed_password=hashed,
        )
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await service.login_user(
            username=None, email="test@test.com", password="pass", db=mock_db
        )
        assert result == user

    @pytest.mark.asyncio
    async def test_get_all_user(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await service.get_all_user(mock_db)
        assert result == []

    @pytest.mark.asyncio
    async def test_get_user_by_id_found(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = User(
            username="test", email="test@test.com", full_name="Test", hashed_password="dummy"
        )
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await service.get_user_by_id(uuid4(), mock_db)
        assert result is not None

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await service.get_user_by_id(uuid4(), mock_db)
        assert result is None

    @pytest.mark.asyncio
    async def test_update_user_success(self, service):
        user_id = uuid4()
        existing = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        mock_db, mock_result = _mock_db_with_user()
        mock_result.scalars.return_value.first.return_value = existing
        mock_db.get = AsyncMock(return_value=existing)

        from app.schemas.user import UserUpdate
        user_in = UserUpdate(full_name="Updated")
        result = await service.update_user(user_id, user_in, mock_db)
        assert result is not None
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, service):
        mock_db, mock_result = _mock_db_with_user()
        mock_result.scalars.return_value.first.return_value = None

        from app.schemas.user import UserUpdate
        user_in = UserUpdate(full_name="Updated")
        with pytest.raises(EntityNotFoundError):
            await service.update_user(uuid4(), user_in, mock_db)

    @pytest.mark.asyncio
    async def test_update_user_duplicate(self, service):
        existing = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        other = User(username="other", email="other@test.com", full_name="Other", hashed_password="dummy")
        mock_db, mock_result = _mock_db_with_user()
        mock_result.scalars.return_value.first.return_value = other
        mock_db.get = AsyncMock(return_value=existing)

        from app.schemas.user import UserUpdate
        user_in = UserUpdate(email="other@test.com")
        with pytest.raises(EntityAlreadyExistsError):
            await service.update_user(uuid4(), user_in, mock_db)

    @pytest.mark.asyncio
    async def test_delete_user_success(self, service):
        user_id = uuid4()
        user = User(username="test", email="t@t.com", full_name="T", hashed_password="dummy")
        mock_db, mock_result = _mock_db_with_user()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.get = AsyncMock(return_value=user)
        mock_db.delete = AsyncMock()

        result = await service.delete_user(user_id, mock_db)
        assert result is True
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, service):
        mock_db, mock_result = _mock_db_with_user()
        mock_result.scalars.return_value.first.return_value = None

        result = await service.delete_user(uuid4(), mock_db)
        assert result is False


def _mock_db_with_user():
    """Module-level helper to create mock db with execute pattern."""
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    mock_db.get = AsyncMock()
    return mock_db, mock_result