from typing import Generic, Optional, TypeVar, TYPE_CHECKING
from sqlalchemy import select
from app.db.base import Base
from app.schemas.iot import IoTDeviceCreate, IoTDeviceUpdate, IoTDeviceSensorCreate, IoTDeviceSensorUpdate, SensorSnapshotCreate, SensorSnapshotBase 
from app.repositories.base import BaseRepository
from app.models.iot import IoTDevice, IoTDeviceSensor, SensorSnapshot

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

class IoTDeviceSensorRepository(BaseRepository[IoTDeviceSensor, IoTDeviceSensorCreate, IoTDeviceSensorUpdate]):
    """Repository for IoTDeviceSensor model."""

    def __init__(self):
        super().__init__(IoTDeviceSensor)


class SensorSnapshotRepository(BaseRepository[SensorSnapshot, SensorSnapshotCreate, SensorSnapshotBase]):
    """Repository for SensorSnapshot model."""

    def __init__(self):
        super().__init__(SensorSnapshot)
    
