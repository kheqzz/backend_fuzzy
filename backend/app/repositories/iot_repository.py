from typing import Generic, TypeVar, TYPE_CHECKING
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

class IoTDeviceSensorRepository(BaseRepository[IoTDeviceSensor, IoTDeviceSensorCreate, IoTDeviceSensorUpdate]):
    """Repository for IoTDeviceSensor model."""

    def __init__(self):
        super().__init__(IoTDeviceSensor)


class SensorSnapshotRepository(BaseRepository[SensorSnapshot, SensorSnapshotCreate, SensorSnapshotBase]):
    """Repository for SensorSnapshot model."""

    def __init__(self):
        super().__init__(SensorSnapshot)
    
