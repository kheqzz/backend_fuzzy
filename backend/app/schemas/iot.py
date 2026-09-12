from pydantic import BaseModel
from uuid import UUID

class IoTDeviceBase(BaseModel):
    name: str
    description: str | None = None
    iot_firmware_version: str

class IoTDeviceCreate(IoTDeviceBase):
    pass

class IoTDeviceOut(IoTDeviceBase):
    iot_id: UUID

    class Config:
        from_attributes = True

class IoTDeviceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    iot_firmware_version: str | None = None
    

class IoTDeviceSensorBase(BaseModel):
    sensor_name: str
    unit: str

class IoTDeviceSensorCreate(IoTDeviceSensorBase):
    pass

class IoTDeviceSensorOut(IoTDeviceSensorBase):
    sensor_id: UUID
    iot_device_id: UUID

    class Config:
        from_attributes = True

class IoTDeviceSensorUpdate(IoTDeviceSensorBase):
    pass

class SensorSnapshotBase(BaseModel):
    sensor_value: float
    fuzzy_value: str

class SensorSnapshotCreate(SensorSnapshotBase):
    pass

class SensorSnapshotOut(SensorSnapshotBase):
    snapshots_id: UUID
    iot_device_id: UUID
    sensor_id: UUID

    class Config:
        from_attributes = True

