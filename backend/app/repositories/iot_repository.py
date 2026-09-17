from typing import Generic, Optional, TypeVar, TYPE_CHECKING
from sqlalchemy import select, join
from app.db.base import Base
from app.schemas.iot import IoTDeviceCreate, IoTDeviceUpdate, IoTDeviceSensorCreate, IoTDeviceSensorUpdate, SensorSnapshotCreate, SensorSnapshotBase 
from app.repositories.base import BaseRepository
from app.models.iot import IoTDevice, IoTDeviceSensor, SensorSnapshot
from uuid import UUID
if TYPE_CHECKING:
    from uuid import UUID


class IoTDeviceRepository(BaseRepository[IoTDevice, IoTDeviceCreate, IoTDeviceUpdate]):
    """Repository for IoTDevice model."""

    def __init__(self):
        super().__init__(IoTDevice)

    async def get_by_id(self, db, device_id: "UUID") -> Optional[IoTDevice]:
        result = await db.execute(
            select(IoTDevice).where(IoTDevice.iot_id == device_id)
        )
        return result.scalars().first()

    async def get_all_devices_by_user_id(self, db, user_id: "UUID") -> list[IoTDevice]:
        result = await db.execute(
            select(IoTDevice).where(IoTDevice.user_id == user_id)
        )
        return result.scalars().all()

class IoTDeviceSensorRepository(BaseRepository[IoTDeviceSensor, IoTDeviceSensorCreate, IoTDeviceSensorUpdate]):
    """Repository for IoTDeviceSensor model."""

    def __init__(self):
        super().__init__(IoTDeviceSensor)

    async def get_by_id(self, db, sensor_id: "UUID") -> Optional[IoTDeviceSensor]:
        result = await db.execute(
            select(IoTDeviceSensor).where(IoTDeviceSensor.sensor_id == sensor_id)
        )
        return result.scalars().first()
    
    async def get_sensor_ownership(self, db, sensor_id: "UUID") -> Optional[UUID]:
        """ 
        Check if the sensor belongs to the current user by joining the IoTDevice and IoTDeviceSensor tables.
        because the IoTDeviceSensor doesnt have a foreign key to the user, but the  sensor have a foreign key to the IoTDevice
        in order to check if the sensor belongs to the current user, 
        we need to join the IoTDevice and IoTDeviceSensor tables and check if the user_id of the IoTDevice matches the current user's id.
        with flow sensor_id -> IoTDeviceSensor.iot_device_id -> IoTDevice.user_id
        """
        result = await db.execute(
             select(IoTDevice.user_id).join(
                  IoTDeviceSensor, IoTDevice.iot_id == IoTDeviceSensor.iot_device_id).where(
                       IoTDeviceSensor.sensor_id == sensor_id)
        )
        return result.scalars().first()

    async def get_all_sensors_by_iot_id(self, db, iot_id: "UUID") -> list[IoTDeviceSensor]:
        result = await db.execute(
            select(IoTDeviceSensor).where(IoTDeviceSensor.iot_device_id == iot_id)
        )
        return result.scalars().all()
class SensorSnapshotRepository(BaseRepository[SensorSnapshot, SensorSnapshotCreate, SensorSnapshotBase]):
    """Repository for SensorSnapshot model."""

    def __init__(self):
        super().__init__(SensorSnapshot)

    async def get_by_id(self, db, snapshot_id: "UUID") -> Optional[SensorSnapshot]:
        result = await db.execute(
            select(SensorSnapshot).where(SensorSnapshot.snapshots_id == snapshot_id)
        )
        return result.scalars().first()
