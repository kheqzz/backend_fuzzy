"""Test BaseRepository."""

from unittest.mock import AsyncMock, MagicMock, ANY
import pytest
from uuid import uuid4
from app.db.base import Base
from app.repositories.base import BaseRepository
from app.models.user import User
from app.models.iot import IoTDevice


class TestBaseRepository:
    """Tests for BaseRepository."""

    @pytest.fixture
    def repo(self):
        return BaseRepository(User)

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    def test_repository_init(self, repo):
        assert repo._query_model == User

    @pytest.mark.asyncio
    async def test_get_uses_db_get(self, repo, mock_db):
        mock_db.get = AsyncMock(return_value=MagicMock())
        await repo.get(mock_db, uuid4())
        mock_db.get.assert_called_once_with(User, ANY)

    @pytest.mark.asyncio
    async def test_get_all_uses_select(self, repo, mock_db):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)
        await repo.get_all(mock_db)
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_dict(self, repo, mock_db):
        mock_db.get = AsyncMock(return_value=None)
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        data = {"username": "test", "email": "test@test.com", "full_name": "Test"}
        await repo.create(mock_db, data)
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_basemodel(self, repo, mock_db):
        from pydantic import BaseModel
        from app.models.user import User
        class TestModel(BaseModel):
            username: str
            email: str
            full_name: str
            hashed_password: str
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        obj = TestModel(
            username="testuser",
            email="test@test.com",
            full_name="Test",
            hashed_password="dummy",
        )
        await repo.create(mock_db, obj)
        mock_db.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_existing(self, repo, mock_db):
        existing = MagicMock()
        mock_db.get = AsyncMock(return_value=existing)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        update_data = {"name": "updated"}
        await repo.update(mock_db, uuid4(), update_data)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_not_found_raises(self, repo, mock_db):
        mock_db.get = AsyncMock(return_value=None)
        with pytest.raises(ValueError):
            await repo.update(mock_db, uuid4(), {"name": "updated"})

    @pytest.mark.asyncio
    async def test_delete_existing_returns_true(self, repo, mock_db):
        mock_db.get = AsyncMock(return_value=MagicMock())
        mock_db.commit = AsyncMock()
        mock_db.delete = AsyncMock()
        result = await repo.delete(mock_db, uuid4())
        assert result is True
        mock_db.delete.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_not_found_returns_false(self, repo, mock_db):
        mock_db.get = AsyncMock(return_value=None)
        result = await repo.delete(mock_db, uuid4())
        assert result is False
        mock_db.delete.assert_not_called()
