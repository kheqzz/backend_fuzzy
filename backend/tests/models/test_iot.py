"""Test IoT models."""

import pytest
from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.iot import IoTDevice, IoTDeviceSensor, SensorSnapshot
from app.models.user import User
from app.db.base import Base
import sqlalchemy as sa


class TestIoTDeviceModel:
    """Tests for IoTDevice model."""

    @pytest.mark.asyncio
    async def test_iot_device_has_uuid(self, db):
        device = IoTDevice(name="Test Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        assert device.iot_id is not None

    @pytest.mark.asyncio
    async def test_iot_device_required_fields(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        assert device.name == "Device"
        assert device.iot_firmware_version == "1.0.0"

    @pytest.mark.asyncio
    async def test_iot_device_optional_description(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", description="Test", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        assert device.description == "Test"

    @pytest.mark.asyncio
    async def test_iot_device_has_timestamps(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        assert device.created_at is not None
        assert device.updated_at is not None

    @pytest.mark.asyncio
    async def test_iot_device_relationship_with_user(self, db):
        user = User(username="testuser", email="test@test.com", full_name="Test", hashed_password="dummy")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        device = IoTDevice(
            user_id=user.id,
            name="Device 1",
            iot_firmware_version="1.0.0",
        )
        db.add(device)
        await db.commit()
        await db.refresh(device)
        assert device.user_id == user.id

    @pytest.mark.asyncio
    async def test_iot_device_cascade_delete_user(self, db):
        user = User(username="testuser", email="test@test.com", full_name="Test", hashed_password="dummy")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        device = IoTDevice(
            user_id=user.id,
            name="Device 1",
            iot_firmware_version="1.0.0",
        )
        db.add(device)
        await db.commit()
        await db.refresh(device)
        await db.delete(user)
        await db.commit()
        result = (await db.execute(select(IoTDevice).where(IoTDevice.iot_id == device.iot_id))).scalars().first()
        assert result is None

    @pytest.mark.asyncio
    async def test_iot_device_has_sensors_relationship(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        # Use selectinload to avoid async lazy loading issues
        result = (await db.execute(
            select(IoTDevice).options(selectinload(IoTDevice.sensors)).where(IoTDevice.iot_id == device.iot_id)
        )).scalars().first()
        assert result.sensors == []

    @pytest.mark.asyncio
    async def test_iot_device_has_snapshot_relationship(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        # Use selectinload to avoid async lazy loading issues
        result = (await db.execute(
            select(IoTDevice).options(selectinload(IoTDevice.snapshot_device)).where(IoTDevice.iot_id == device.iot_id)
        )).scalars().first()
        assert result.snapshot_device == []


class TestIoTDeviceSensorModel:
    """Tests for IoTDeviceSensor model."""

    @pytest.mark.asyncio
    async def test_sensor_has_uuid(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(
            iot_device_id=device.iot_id,
            sensor_name="Temperature",
            unit="Celsius",
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        assert sensor.sensor_id is not None

    @pytest.mark.asyncio
    async def test_sensor_required_fields(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(
            iot_device_id=device.iot_id,
            sensor_name="Humidity",
            unit="Percent",
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        assert sensor.sensor_name == "Humidity"
        assert sensor.unit == "Percent"

    @pytest.mark.asyncio
    async def test_sensor_has_timestamps(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(
            iot_device_id=device.iot_id,
            sensor_name="Temp",
            unit="C",
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        assert sensor.created_at is not None
        assert sensor.updated_at is not None

    @pytest.mark.asyncio
    async def test_sensor_relationship_with_iot_device(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(
            iot_device_id=device.iot_id,
            sensor_name="Temperature",
            unit="Celsius",
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        assert sensor.iot_device_id == device.iot_id

    @pytest.mark.asyncio
    async def test_sensor_cascade_delete_device(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(
            iot_device_id=device.iot_id,
            sensor_name="Temp",
            unit="C",
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        await db.delete(device)
        await db.commit()
        result = (await db.execute(select(IoTDeviceSensor).where(IoTDeviceSensor.sensor_id == sensor.sensor_id))).scalars().first()
        assert result is None

    @pytest.mark.asyncio
    async def test_sensor_has_snapshot_relationship(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(sensor_name="Temp", unit="C", iot_device_id=device.iot_id)
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        # Use selectinload to avoid async lazy loading issues
        result = (await db.execute(
            select(IoTDeviceSensor).options(selectinload(IoTDeviceSensor.snapshot_sensor)).where(IoTDeviceSensor.sensor_id == sensor.sensor_id)
        )).scalars().first()
        assert result.snapshot_sensor == []


class TestSensorSnapshotModel:
    """Tests for SensorSnapshot model."""

    @pytest.mark.asyncio
    async def test_snapshot_has_uuid(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(
            iot_device_id=device.iot_id,
            sensor_name="Temperature",
            unit="Celsius",
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        from datetime import datetime
        snapshot = SensorSnapshot(
            sensor_value=25.0, fuzzy_value="medium",
            iot_device_id=device.iot_id,
            sensor_id=sensor.sensor_id,
            created_at=datetime.now(),
        )
        db.add(snapshot)
        await db.commit()
        await db.refresh(snapshot)
        assert snapshot.snapshots_id is not None

    @pytest.mark.asyncio
    async def test_snapshot_required_fields(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(
            iot_device_id=device.iot_id,
            sensor_name="Temperature",
            unit="Celsius",
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        from datetime import datetime
        snapshot = SensorSnapshot(
            sensor_value=30.0, fuzzy_value="high",
            iot_device_id=device.iot_id,
            sensor_id=sensor.sensor_id,
            created_at=datetime.now(),
        )
        db.add(snapshot)
        await db.commit()
        await db.refresh(snapshot)
        assert snapshot.sensor_value == 30.0
        assert snapshot.fuzzy_value == "high"

    @pytest.mark.asyncio
    async def test_snapshot_fuzzy_value(self, db):
        device = IoTDevice(name="Device", iot_firmware_version="1.0.0", user_id=UUID("00000000-0000-0000-0000-000000000000"))
        db.add(device)
        await db.commit()
        await db.refresh(device)
        sensor = IoTDeviceSensor(
            iot_device_id=device.iot_id,
            sensor_name="Temperature",
            unit="Celsius",
        )
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        from datetime import datetime
        snapshot = SensorSnapshot(
            sensor_value=20.0, fuzzy_value="low",
            iot_device_id=device.iot_id,
            sensor_id=sensor.sensor_id,
            created_at=datetime.now(),
        )
        db.add(snapshot)
        await db.commit()
        await db.refresh(snapshot)
        assert snapshot.fuzzy_value == "low"