"""Test base classes."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from pydantic import BaseModel

from app.repositories.base import BaseRepository, BaseSchema, PydanticBaseModel
from app.services.base import BaseService


class TestBaseRepository:
    """Tests for BaseRepository."""

    def test_base_repository_init(self):
        model = MagicMock()
        repo = BaseRepository(model)
        assert repo._query_model == model

    @pytest.mark.asyncio
    async def test_base_repository_get(self):
        model_mock = MagicMock()
        repo = BaseRepository(model_mock)
        db = MagicMock()
        db.get = AsyncMock(return_value=MagicMock())
        await repo.get(db, "some-id")
        db.get.assert_called_once_with(model_mock, "some-id")

    @pytest.mark.asyncio
    async def test_base_repository_get_all(self):
        from app.models.user import User
        repo = BaseRepository(User)
        db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        db.execute = AsyncMock(return_value=mock_result)
        await repo.get_all(db)

    @pytest.mark.asyncio
    async def test_base_repository_create_with_dict(self):
        model_mock = MagicMock()
        repo = BaseRepository(model_mock)
        db = MagicMock()
        db.commit = AsyncMock()
        db.refresh = AsyncMock()
        await repo.create(db, {"name": "test"})
        db.add.assert_called_once()
        db.commit.assert_called_once()
        db.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_repository_create_with_basemodel(self):
        model_mock = MagicMock()
        repo = BaseRepository(model_mock)
        db = MagicMock()
        db.commit = AsyncMock()
        db.refresh = AsyncMock()
        class TestModel(BaseModel):
            name: str
        obj = TestModel(name="test")
        await repo.create(db, obj)
        db.add.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_repository_update(self):
        model_mock = MagicMock()
        repo = BaseRepository(model_mock)
        db = MagicMock()
        db.get = AsyncMock(return_value=MagicMock())
        db.commit = AsyncMock()
        db.refresh = AsyncMock()
        class UpdateModel(BaseModel):
            name: str
        update_obj = UpdateModel(name="updated")
        await repo.update(db, "id", update_obj)
        db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_repository_delete_existing(self):
        model_mock = MagicMock()
        repo = BaseRepository(model_mock)
        db = MagicMock()
        db.get = AsyncMock(return_value=MagicMock())
        db.delete = AsyncMock()
        db.commit = AsyncMock()
        result = await repo.delete(db, "id")
        assert result is True
        db.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_repository_delete_not_found(self):
        model_mock = MagicMock()
        repo = BaseRepository(model_mock)
        db = MagicMock()
        db.get = AsyncMock(return_value=None)
        result = await repo.delete(db, "id")
        assert result is False


class TestBaseService:
    """Tests for BaseService."""

    def test_base_service_init(self):
        repo = MagicMock()
        service = BaseService(repo)
        assert service.repository == repo

    @pytest.mark.asyncio
    async def test_base_service_get(self):
        repo = MagicMock()
        repo.get = AsyncMock(return_value=MagicMock())
        service = BaseService(repo)
        await service.get(MagicMock(), "id")
        repo.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_service_get_all(self):
        repo = MagicMock()
        repo.get_all = AsyncMock(return_value=[])
        service = BaseService(repo)
        await service.get_all(MagicMock())
        repo.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_service_create(self):
        repo = MagicMock()
        repo.create = AsyncMock(return_value=MagicMock())
        service = BaseService(repo)
        await service.create(MagicMock(), {"key": "value"})
        repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_service_update(self):
        repo = MagicMock()
        repo.update = AsyncMock(return_value=MagicMock())
        service = BaseService(repo)
        await service.update(MagicMock(), {"key": "value"})
        repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_service_delete(self):
        repo = MagicMock()
        repo.delete = AsyncMock(return_value=True)
        service = BaseService(repo)
        await service.delete(MagicMock(), "id")
        repo.delete.assert_called_once()


class TestBaseSchema:
    """Tests for BaseSchema."""

    def test_base_schema_allows_extra(self):
        schema = BaseSchema()
        schema.extra_field = "test"
        assert schema.extra_field == "test"


class TestPydanticBaseModel:
    """Tests for PydanticBaseModel."""

    def test_model_dump_works(self):
        class TestModel(PydanticBaseModel):
            name: str = "test"

        model = TestModel()
        result = model.model_dump()
        assert result == {"name": "test"}
