from uuid import UUID
from datetime import datetime
from typing import Optional, Sequence, Any
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService
from app.core import exceptions as ex
from app.repositories.iot_repository import IoTDeviceRepository, IoTDeviceSensorRepository, SensorSnapshotRepository
from app.models.iot import IoTDevice, IoTDeviceSensor, SensorSnapshot


class IoTDeviceService(BaseService[IoTDeviceRepository]):
    """
    Service layer for IoT operations.

    All business logic related to IoT devices, sensors, and snapshots should go here:
    - Creating/updating/deleting devices and sensors
    - Retrieving device and sensor data
    """

    def __init__(self, iot_repo: IoTDeviceRepository):
        super().__init__(iot_repo)

    async def add_device(self, db: AsyncSession, device_data: dict[str, Any], user_id: UUID) -> "IoTDevice":
        """
        Add a new IoT device to the database.
        """
        device_data['user_id'] = user_id
        return await self.repository.create(db, device_data)

    async def get_all_devices(self, db: AsyncSession) -> Sequence["IoTDevice"]:
        """
        Retrieve all IoT devices from the database.
        """
        return await self.repository.get_all(db)

    async def get_all_devices_by_user_id(self, db: AsyncSession, user_id: UUID) -> Sequence["IoTDevice"]:
        """
        Retrieve all IoT devices associated with a specific user ID.
        """
        devices = await self.repository.get_all_devices_by_user_id(db, user_id)
        if not devices:
            raise ex.IoTNotFoundError(entity_id=user_id, entity_name="IoTDevice")
        return devices

    async def get_device_by_id(self, db: AsyncSession, device_id: UUID) -> Optional["IoTDevice"]:
        """
        Retrieve an IoT device by its ID.
        """
        device = await self.repository.get_by_id(db, device_id)
        if not device:
            raise ex.EntityNotFoundError(entity_id=device_id, entity_name="IoTDevice")
        return device

    async def update_device(self, db: AsyncSession, device_id: UUID, device_data: dict[str, Any]) -> "IoTDevice":
        """
        Update an existing IoT device in the database.
        """
        device = await self.get_device_by_id(db, device_id)
        if not device:
            raise ex.EntityNotFoundError(entity_id=device_id, entity_name="IoTDevice")
        updated_device = await self.repository.update(db, device_id, device_data)
        return updated_device

    async def delete_device(self, db: AsyncSession, device_id: UUID) -> bool:
        """
        Delete an IoT device from the database.
        """
        device = await self.get_device_by_id(db, device_id)
        if not device:
            raise ex.EntityNotFoundError(entity_id=device_id, entity_name="IoTDevice")
        return await self.repository.delete(db, device_id)

    async def get_device_name_by_id(self, db: AsyncSession, device_id: UUID) -> str:
        """
        Retrieve the name of an IoT device by its ID.
        """
        device = await self.get_device_by_id(db, device_id)
        if not device:
            raise ex.EntityNotFoundError(entity_id=device_id, entity_name="IoTDevice")
        return device.name

class IoTSensorService(BaseService[IoTDeviceSensorRepository]):
    """
    Service layer for IoT Sensor operations.

    All business logic related to IoT sensors should go here:
    - Creating/updating/deleting sensors
    - Retrieving sensor data
    """

    def __init__(self, sensor_repo: IoTDeviceSensorRepository):
        super().__init__(sensor_repo)

    async def add_sensor(self, db: AsyncSession, sensor_data: dict[str, Any], device_id: UUID) -> "IoTDeviceSensor":
        """
        Add a new IoT sensor to the database.
        """
        sensor_data["iot_device_id"] = device_id
        return await self.repository.create(db, sensor_data)

    async def get_all_sensors(self, db: AsyncSession) -> Sequence["IoTDeviceSensor"]:
        """
        Retrieve all IoT sensors from the database.
        """
        return await self.repository.get_all(db)

    async def get_sensor_by_id(self, db: AsyncSession, sensor_id: UUID) -> Optional["IoTDeviceSensor"]:
        """
        Retrieve an IoT sensor by its ID.
        """
        sensor = await self.repository.get_by_id(db, sensor_id)
        if not sensor:
            raise ex.EntityNotFoundError(entity_id=sensor_id, entity_name="IoTDeviceSensor")
        return sensor

    async def check_sensor_ownership(self, db:AsyncSession, sensor_id: UUID, user_id: UUID) -> Optional[UUID]:
        """
        Check if the sensor belongs to the current user.
        """
        owner = await self.repository.get_sensor_ownership(db, sensor_id)
       
        return owner

    async def get_all_sensors_by_iot_id(self, db: AsyncSession, iot_id: UUID) -> Sequence["IoTDeviceSensor"]:
        """
        Retrieve all IoT sensors associated with a specific IoT device ID.
        """
        sensors = await self.repository.get_all_sensors_by_iot_id(db, iot_id)
        if not sensors:
            raise ex.EntityNotFoundError(entity_id=iot_id, entity_name="IoTDevice")
        return sensors
    
    async def update_sensor(self, db: AsyncSession, sensor_id: UUID, sensor_data: dict[str, Any]) -> "IoTDeviceSensor":
        """
        Update an existing IoT sensor in the database.
        """
        sensor = await self.get_sensor_by_id(db, sensor_id)
        if not sensor:
            raise ex.EntityNotFoundError(entity_id=sensor_id, entity_name="IoTDeviceSensor")
        updated_sensor = await self.repository.update(db, sensor_id, sensor_data)
        return updated_sensor

    async def delete_sensor(self, db: AsyncSession, sensor_id: UUID) -> bool:
        """
        Delete an IoT sensor from the database.
        """
        sensor = await self.get_sensor_by_id(db, sensor_id)
        if not sensor:
            raise ex.EntityNotFoundError(entity_id=sensor_id, entity_name="IoTDeviceSensor")
        return await self.repository.delete(db, sensor_id)

class SnapshotService(BaseService[SensorSnapshotRepository]):
    """
    Service layer for Sensor Snapshot operations.

    All business logic related to sensor snapshots should go here:
    - Creating/updating/deleting snapshots
    - Retrieving snapshot data
    """

    def __init__(self, snapshot_repo: SensorSnapshotRepository):
        super().__init__(snapshot_repo)

    async def add_snapshot(self, db: AsyncSession, snapshot_data: dict[str, Any]) -> "SensorSnapshot":
        """
        Add a new sensor snapshot to the database.
        """
        return await self.repository.create(db, snapshot_data)

    async def get_all_snapshots(self, db: AsyncSession) -> Sequence["SensorSnapshot"]:
        """
        Retrieve all sensor snapshots from the database.
        """
        return await self.repository.get_all(db)