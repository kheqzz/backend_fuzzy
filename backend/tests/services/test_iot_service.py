"""Test IoTSensorService."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from uuid import uuid4
from app.services.iot_service import IoTSensorService
from app.models.iot import IoTDeviceSensor
from app.core.exceptions import EntityNotFoundError
from app.repositories.iot_repository import IoTDeviceSensorRepository


class TestIoTSensorService:
    """Tests for IoTSensorService."""

    @pytest.fixture
    def service(self):
        return IoTSensorService(IoTDeviceSensorRepository())

    @pytest.mark.asyncio
    async def test_add_sensor(self, service):
        mock_db = MagicMock()
        mock_db.execute = AsyncMock(return_value=MagicMock())
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.add = MagicMock()

        result = await service.add_sensor(
            mock_db, {"sensor_name": "Temp", "unit": "C"}, uuid4()
        )
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_sensors(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await service.get_all_sensors(mock_db)
        assert result == []

    @pytest.mark.asyncio
    async def test_get_sensor_by_id_found(self, service):
        mock_db = MagicMock()
        sensor = IoTDeviceSensor(sensor_name="Temp", unit="C")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = sensor
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await service.get_sensor_by_id(mock_db, uuid4())
        assert result == sensor

    @pytest.mark.asyncio
    async def test_get_sensor_by_id_not_found(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        with pytest.raises(EntityNotFoundError):
            await service.get_sensor_by_id(mock_db, uuid4())

    @pytest.mark.asyncio
    async def test_check_sensor_ownership(self, service):
        mock_db = MagicMock()
        user_id = uuid4()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = user_id
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await service.check_sensor_ownership(mock_db, uuid4(), user_id)
        assert result == user_id

    @pytest.mark.asyncio
    async def test_get_all_sensors_by_iot_id_found(self, service):
        mock_db = MagicMock()
        sensor = IoTDeviceSensor(sensor_name="Temp", unit="C")
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sensor]
        mock_db.execute = AsyncMock(return_value=mock_result)
        result = await service.get_all_sensors_by_iot_id(mock_db, uuid4())
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_all_sensors_by_iot_id_not_found(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)
        with pytest.raises(EntityNotFoundError):
            await service.get_all_sensors_by_iot_id(mock_db, uuid4())

    @pytest.mark.asyncio
    async def test_update_sensor(self, service):
        mock_db = MagicMock()
        sensor = IoTDeviceSensor(sensor_name="Temp", unit="C")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = sensor
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.get = AsyncMock(return_value=sensor)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        result = await service.update_sensor(mock_db, uuid4(), {"sensor_name": "Humidity"})
        assert result is not None

    @pytest.mark.asyncio
    async def test_update_sensor_not_found(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        with pytest.raises(EntityNotFoundError):
            await service.update_sensor(mock_db, uuid4(), {"sensor_name": "Humidity"})

    @pytest.mark.asyncio
    async def test_delete_sensor(self, service):
        mock_db = MagicMock()
        sensor = IoTDeviceSensor(sensor_name="Temp", unit="C")
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = sensor
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.get = AsyncMock(return_value=sensor)
        mock_db.delete = AsyncMock()
        mock_db.commit = AsyncMock()
        result = await service.delete_sensor(mock_db, uuid4())
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_sensor_not_found(self, service):
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)
        with pytest.raises(EntityNotFoundError):
            await service.delete_sensor(mock_db, uuid4())