"""Test SnapshotService."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from uuid import uuid4
from app.services.iot_service import SnapshotService
from app.models.iot import SensorSnapshot
from app.repositories.iot_repository import SensorSnapshotRepository


class TestSnapshotService:
    """Tests for SnapshotService."""

    @pytest.fixture
    def service(self):
        return SnapshotService(SensorSnapshotRepository())

    @pytest.mark.asyncio
    async def test_add_snapshot(self, service):
        mock_db = MagicMock()
        mock_db.execute = AsyncMock(return_value=MagicMock())
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.add = MagicMock()

        result = await service.add_snapshot(mock_db, {"sensor_value": 25.0, "fuzzy_value": "medium"})
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_snapshots(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await service.get_all_snapshots(mock_db)
        assert result == []
