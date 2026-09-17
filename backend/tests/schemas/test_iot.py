"""Test IoT schemas."""

import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from app.schemas.iot import (
    IoTDeviceBase,
    IoTDeviceCreate,
    IoTDeviceOut,
    IoTDeviceUpdate,
    IoTDeviceSensorBase,
    IoTDeviceSensorCreate,
    IoTDeviceSensorOut,
    IoTDeviceSensorUpdate,
    SensorSnapshotBase,
    SensorSnapshotCreate,
    SensorSnapshotOut,
)


class TestIoTDeviceBase:
    """Tests for IoTDeviceBase schema."""

    def test_iot_device_base_valid(self):
        data = {
            "name": "Test Device",
            "description": "A test device",
            "iot_firmware_version": "1.0.0",
        }
        schema = IoTDeviceBase(**data)
        assert schema.name == "Test Device"
        assert schema.description == "A test device"
        assert schema.iot_firmware_version == "1.0.0"

    def test_iot_device_base_description_optional(self):
        data = {
            "name": "Test Device",
            "iot_firmware_version": "1.0.0",
        }
        schema = IoTDeviceBase(**data)
        assert schema.description is None

    def test_iot_device_base_name_required(self):
        with pytest.raises(ValidationError):
            IoTDeviceBase(description="test", iot_firmware_version="1.0.0")

    def test_iot_device_base_firmware_required(self):
        with pytest.raises(ValidationError):
            IoTDeviceBase(name="test", description="test")


class TestIoTDeviceCreate:
    """Tests for IoTDeviceCreate schema."""

    def test_iot_device_create_valid(self):
        data = {
            "name": "Device 1",
            "description": "First device",
            "iot_firmware_version": "2.1.0",
        }
        schema = IoTDeviceCreate(**data)
        assert schema.name == "Device 1"

    def test_iot_device_create_minimal(self):
        data = {
            "name": "Device 1",
            "iot_firmware_version": "1.0.0",
        }
        schema = IoTDeviceCreate(**data)
        assert schema.name == "Device 1"


class TestIoTDeviceOut:
    """Tests for IoTDeviceOut schema."""

    def test_iot_device_out_valid(self):
        data = {
            "iot_id": uuid4(),
            "name": "Device 1",
            "description": "First device",
            "iot_firmware_version": "1.0.0",
        }
        schema = IoTDeviceOut(**data)
        assert schema.iot_id == data["iot_id"]
        assert schema.name == "Device 1"

    def test_iot_device_out_from_attributes(self):
        class FakeDevice:
            iot_id = uuid4()
            name = "Device 1"
            description = "Test"
            iot_firmware_version = "1.0.0"

        schema = IoTDeviceOut.model_validate(FakeDevice())
        assert schema.iot_id is not None
        assert schema.name == "Device 1"


class TestIoTDeviceUpdate:
    """Tests for IoTDeviceUpdate schema."""

    def test_iot_device_update_all_fields(self):
        data = {
            "name": "Updated",
            "description": "Updated desc",
            "iot_firmware_version": "3.0.0",
        }
        schema = IoTDeviceUpdate(**data)
        assert schema.name == "Updated"

    def test_iot_device_update_partial(self):
        schema = IoTDeviceUpdate(name="New Name")
        assert schema.name == "New Name"
        assert schema.description is None
        assert schema.iot_firmware_version is None

    def test_iot_device_update_all_none(self):
        schema = IoTDeviceUpdate()
        assert schema.name is None


class TestIoTDeviceSensorBase:
    """Tests for IoTDeviceSensorBase schema."""

    def test_sensor_base_valid(self):
        data = {"sensor_name": "Temperature", "unit": "Celsius"}
        schema = IoTDeviceSensorBase(**data)
        assert schema.sensor_name == "Temperature"
        assert schema.unit == "Celsius"

    def test_sensor_base_name_required(self):
        with pytest.raises(ValidationError):
            IoTDeviceSensorBase(unit="Celsius")

    def test_sensor_base_unit_required(self):
        with pytest.raises(ValidationError):
            IoTDeviceSensorBase(sensor_name="Temperature")


class TestIoTDeviceSensorCreate:
    """Tests for IoTDeviceSensorCreate schema."""

    def test_sensor_create_valid(self):
        data = {"sensor_name": "Humidity", "unit": "Percent"}
        schema = IoTDeviceSensorCreate(**data)
        assert schema.sensor_name == "Humidity"


class TestIoTDeviceSensorOut:
    """Tests for IoTDeviceSensorOut schema."""

    def test_sensor_out_valid(self):
        data = {
            "sensor_id": uuid4(),
            "iot_device_id": uuid4(),
            "sensor_name": "Temperature",
            "unit": "Celsius",
        }
        schema = IoTDeviceSensorOut(**data)
        assert schema.sensor_id == data["sensor_id"]
        assert schema.iot_device_id == data["iot_device_id"]

    def test_sensor_out_from_attributes(self):
        class FakeSensor:
            sensor_id = uuid4()
            iot_device_id = uuid4()
            sensor_name = "Temp"
            unit = "C"

        schema = IoTDeviceSensorOut.model_validate(FakeSensor())
        assert schema.sensor_id is not None


class TestIoTDeviceSensorUpdate:
    """Tests for IoTDeviceSensorUpdate schema."""

    def test_sensor_update_valid(self):
        schema = IoTDeviceSensorUpdate(sensor_name="Updated", unit="Celsius")
        assert schema.sensor_name == "Updated"
        assert schema.unit == "Celsius"


class TestSensorSnapshotBase:
    """Tests for SensorSnapshotBase schema."""

    def test_snapshot_base_valid(self):
        data = {"sensor_value": 25.5, "fuzzy_value": "medium"}
        schema = SensorSnapshotBase(**data)
        assert schema.sensor_value == 25.5
        assert schema.fuzzy_value == "medium"

    def test_snapshot_base_value_required(self):
        with pytest.raises(ValidationError):
            SensorSnapshotBase(fuzzy_value="medium")


class TestSensorSnapshotCreate:
    """Tests for SensorSnapshotCreate schema."""

    def test_snapshot_create_valid(self):
        data = {"sensor_value": 30.0, "fuzzy_value": "high"}
        schema = SensorSnapshotCreate(**data)
        assert schema.sensor_value == 30.0


class TestSensorSnapshotOut:
    """Tests for SensorSnapshotOut schema."""

    def test_snapshot_out_valid(self):
        data = {
            "snapshots_id": uuid4(),
            "iot_device_id": uuid4(),
            "sensor_id": uuid4(),
            "sensor_value": 25.5,
            "fuzzy_value": "medium",
        }
        schema = SensorSnapshotOut(**data)
        assert schema.snapshots_id == data["snapshots_id"]