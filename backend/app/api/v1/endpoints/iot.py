from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import exceptions as ex

from app.models.iot import IoTDevice, IoTDeviceSensor, SensorSnapshot
from app.schemas.iot import IoTDeviceCreate, IoTDeviceOut, IoTDeviceSensorOut, IoTDeviceUpdate, IoTDeviceSensorCreate, IoTDeviceSensorUpdate, SensorSnapshotCreate, SensorSnapshotBase
from app.services.iot_service import IoTDeviceService, IoTSensorService
from app.db.dependencies import get_async_session
from app.api.deps import get_current_user, getIoTDeviceSensorService, getIoTDeviceService
from app.models.user import User
from uuid import UUID

router = APIRouter()

@router.post("/devices", response_model=IoTDeviceOut)
async def create_iot_device(
    device_in: IoTDeviceCreate,
    iot_service: IoTDeviceService = Depends(getIoTDeviceService),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new IoT device."""
    device = await iot_service.add_device(db, device_in.model_dump(), user_id=current_user.id)
    return device

@router.get("/devices", response_model=list[IoTDeviceOut])
async def get_iot_devices(
    iot_service: IoTDeviceService = Depends(getIoTDeviceService),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get all IoT devices."""
    devices = await iot_service.get_all_devices_by_user_id(db,user_id=current_user.id)
    return devices

@router.get("/devices/{device_id}", response_model=IoTDeviceOut)
async def get_iot_device(
    device_id: UUID,
    iot_service: IoTDeviceService = Depends(getIoTDeviceService),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific IoT device by ID."""
    device = await iot_service.get_device_by_id(db, device_id)
    if not device:
        raise ex.EntityNotFoundError(entity_name="IoTDevice", entity_id=device_id)
    return device

@router.put("/devices/{device_id}", response_model=IoTDeviceOut)
async def update_iot_device(
    device_id: UUID,
    device_in: IoTDeviceUpdate,
    iot_service: IoTDeviceService = Depends(getIoTDeviceService),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Update an existing IoT device."""
    device = await iot_service.update_device(db, device_id, device_in.model_dump(exclude_unset=True))
    if not device:
        raise ex.EntityNotFoundError(entity_name="IoTDevice", entity_id=device_id)
    return device

@router.delete("/devices/{device_id}")
async def delete_iot_device(
    device_id: UUID,
    iot_service: IoTDeviceService = Depends(getIoTDeviceService),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Delete an existing IoT device."""
    device = await iot_service.delete_device(db, device_id)
    if not device:
        raise ex.EntityNotFoundError(entity_name="IoTDevice", entity_id=device_id)
    return device

@router.post('/devices/{device_id}/sensors', response_model=IoTDeviceSensorOut)
async def create_iot_device_sensor(
    device_id: UUID,
    sensor_in: IoTDeviceSensorCreate,
    sensor_service:IoTSensorService = Depends(getIoTDeviceSensorService),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new sensor for a specific IoT device."""
    sensor = await sensor_service.add_sensor(db, sensor_in.model_dump(), device_id)
    return sensor

@router.get('/devices/{device_id}/sensors', response_model=list[IoTDeviceSensorOut])
async def get_iot_device_sensors(
    device_id: UUID,
    sensor_service: IoTSensorService = Depends(getIoTDeviceSensorService),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Get all sensors for a specific IoT device."""
    sensors = await sensor_service.get_all_sensors_by_iot_id(db, device_id)
    return sensors

@router.delete('/sensors/{sensor_id}', response_model=IoTDeviceSensorOut)
async def delete_iot_device_sensor(
    sensor_id: UUID,
    sensor_service: IoTSensorService = Depends(getIoTDeviceSensorService),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific sensor by ID."""
    sensor = await sensor_service.delete_sensor(db, sensor_id)
    if not sensor:
        raise ex.EntityNotFoundError(entity_name="IoTDeviceSensor", entity_id=sensor_id)
    return sensor
