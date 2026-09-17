"""Test IoTRepository."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from sqlalchemy import select
from app.repositories.iot_repository import (
    IoTDeviceRepository,
    IoTDeviceSensorRepository,
    SensorSnapshotRepository,
)
from app.models.iot import IoTDevice, IoTDeviceSensor, SensorSnapshot
from app.models.user import User


class TestIoTDeviceRepository:
    """Tests for IoTDeviceRepository."""

    @pytest.fixture
    def repo(self):
        return IoTDeviceRepository()

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, mock_db):
        device = IoTDevice(name="Test", iot_firmware_version="1.0.0", user_id="00000000-0000-0000-0000-000000000000")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = device
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_id(mock_db, uuid4())
        assert result == device

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, mock_db):
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_id(mock_db, uuid4())
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_devices_by_user_id(self, repo, mock_db):
        device1 = IoTDevice(name="Device 1", iot_firmware_version="1.0.0", user_id="00000000-0000-0000-0000-000000000000")
        device2 = IoTDevice(name="Device 2", iot_firmware_version="2.0.0", user_id="00000000-0000-0000-0000-000000000000")
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [device1, device2]
        mock_db.execute = AsyncMock(return_value=mock_result)
        user_id = uuid4()
        result = await repo.get_all_devices_by_user_id(mock_db, user_id)
        assert len(result) == 2
        mock_db.execute.assert_called_once()
        call_args = mock_db.execute.call_args[0][0]
        assert str(call_args).startswith("SELECT")


class TestIoTDeviceSensorRepository:
    """Tests for IoTDeviceSensorRepository."""

    @pytest.fixture
    def repo(self):
        return IoTDeviceSensorRepository()

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, mock_db):
        sensor = IoTDeviceSensor(sensor_name="Temp", unit="C", iot_device_id="00000000-0000-0000-0000-000000000000")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = sensor
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_id(mock_db, uuid4())
        assert result == sensor

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, mock_db):
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_id(mock_db, uuid4())
        assert result is None

    @pytest.mark.asyncio
    async def test_get_sensor_ownership_found(self, repo, mock_db):
        user_id = uuid4()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user_id
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_sensor_ownership(mock_db, uuid4())
        assert result == user_id

    @pytest.mark.asyncio
    async def test_get_sensor_ownership_not_found(self, repo, mock_db):
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_sensor_ownership(mock_db, uuid4())
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_sensors_by_iot_id(self, repo, mock_db):
        sensor1 = IoTDeviceSensor(sensor_name="Temp", unit="C", iot_device_id="00000000-0000-0000-0000-000000000000")
        sensor2 = IoTDeviceSensor(sensor_name="Humidity", unit="%", iot_device_id="00000000-0000-0000-0000-000000000000")
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sensor1, sensor2]
        mock_db.execute = AsyncMock(return_value=mock_result)
        iot_id = uuid4()
        result = await repo.get_all_sensors_by_iot_id(mock_db, iot_id)
        assert len(result) == 2


class TestSensorSnapshotRepository:
    """Tests for SensorSnapshotRepository."""

    @pytest.fixture
    def repo(self):
        return SensorSnapshotRepository()

    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    def test_repository_init(self, repo):
        assert repo._query_model == SensorSnapshot

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repo, mock_db):
        from uuid import uuid4
        snapshot = SensorSnapshot(
            sensor_value=25.0, fuzzy_value="medium",
            iot_device_id="00000000-0000-0000-0000-000000000000",
            sensor_id="00000000-0000-0000-0000-000000000001",
        )
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = snapshot
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_id(mock_db, uuid4())
        assert result == snapshot

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repo, mock_db):
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await repo.get_by_id(mock_db, uuid4())
        assert result is None