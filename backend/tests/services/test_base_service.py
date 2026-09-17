"""Test BaseService."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from app.services.base import BaseService


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
        result = await service.get(MagicMock(), "id")
        repo.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_service_get_all(self):
        repo = MagicMock()
        repo.get_all = AsyncMock(return_value=[])
        service = BaseService(repo)
        result = await service.get_all(MagicMock())
        assert result == []

    @pytest.mark.asyncio
    async def test_base_service_create(self):
        repo = MagicMock()
        repo.create = AsyncMock(return_value=MagicMock())
        service = BaseService(repo)
        result = await service.create(MagicMock(), {})
        repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_service_update(self):
        repo = MagicMock()
        repo.update = AsyncMock(return_value=MagicMock())
        service = BaseService(repo)
        result = await service.update(MagicMock(), {})
        repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_base_service_delete(self):
        repo = MagicMock()
        repo.delete = AsyncMock(return_value=True)
        service = BaseService(repo)
        result = await service.delete(MagicMock(), "id")
        repo.delete.assert_called_once()
