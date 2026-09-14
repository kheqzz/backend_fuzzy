from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_async_session
from app.core.security import decode_access_token
from app import db
from app.core.exceptions import EntityNotFoundError as ex
from app.models.iot import IoTDevice, IoTDeviceSensor, SensorSnapshot
from app.models.user import User
from app.repositories.iot_repository import IoTDeviceRepository, IoTDeviceSensorRepository, SensorSnapshotRepository
from app.services.iot_service import IoTDeviceService, IoTSensorService, SensorSnapshot, IoTDeviceSensor, SnapshotService


def get_user_service() -> UserService:
    return UserService(UserRepository())

def getIoTDeviceService() -> IoTDeviceService:
    return IoTDeviceService(IoTDeviceRepository())

def getSensorSnapshotService() -> SnapshotService:
    return SnapshotService(SensorSnapshotRepository())

def getIoTDeviceSensorService() -> IoTSensorService:
    return IoTSensorService(IoTDeviceSensorRepository())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
dbDeps = Annotated[AsyncSession, Depends(get_async_session)]
userServiceDeps = Annotated[UserService, Depends(get_user_service)]
tokenDeps = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(token : tokenDeps, db : dbDeps, user_service :userServiceDeps) -> User :
    """
    Dependency to get the current authenticated user.
    """
    userId = decode_access_token(token=token)
    user = await user_service.get_user_by_id(userId, db)
    if not user:
        raise ex(entity_id=userId, entity_name="User")
    return user