"""Test UserRepository."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from sqlalchemy import select
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.exceptions import EntityNotFoundError


class TestUserRepository:
    """Tests for UserRepository."""

    @pytest.fixture
    def repo(self):
        return UserRepository()

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.mark.asyncio
    async def test_get_by_email_found(self, repo, mock_db):
        user = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_email(mock_db, "test@test.com")
        assert result == user

    @pytest.mark.asyncio
    async def test_get_by_email_not_found(self, repo, mock_db):
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_email(mock_db, "nonexistent@test.com")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_username_found(self, repo, mock_db):
        user = User(username="testuser", email="test@test.com", full_name="Test", hashed_password="dummy")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_username(mock_db, "testuser")
        assert result == user

    @pytest.mark.asyncio
    async def test_get_by_username_not_found(self, repo, mock_db):
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_username(mock_db, "nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_username_or_email_with_both(self, repo, mock_db):
        user = User(username="testuser", email="test@test.com", full_name="Test", hashed_password="dummy")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_username_or_email(
            mock_db, username="testuser", email="test@test.com"
        )
        assert result == user

    @pytest.mark.asyncio
    async def test_get_by_username_or_email_with_username_only(self, repo, mock_db):
        user = User(username="testuser", email="test@test.com", full_name="Test", hashed_password="dummy")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_username_or_email(mock_db, username="testuser")
        assert result == user

    @pytest.mark.asyncio
    async def test_get_by_username_or_email_with_email_only(self, repo, mock_db):
        user = User(username="testuser", email="test@test.com", full_name="Test", hashed_password="dummy")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_username_or_email(mock_db, email="test@test.com")
        assert result == user

    @pytest.mark.asyncio
    async def test_get_by_username_or_email_neither(self, repo, mock_db):
        result = await repo.get_by_username_or_email(mock_db)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, mock_db):
        user = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_id(mock_db, uuid4())
        assert result == user

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, mock_db):
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_id(mock_db, uuid4())
        assert result is None