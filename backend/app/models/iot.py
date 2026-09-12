import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class IoTDevice(Base):
    """IoT Device model."""

    __tablename__ = "iot_devices"

    iot_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),)
    iot_firmware_version: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    sensors: Mapped[List['IoTDeviceSensor']] = relationship("IoTDeviceSensor", back_populates="iot_device", cascade="all, delete-orphan")
    snapshot_device: Mapped[List['SensorSnapshot']] = relationship("SensorSnapshot", back_populates="iot_device_snapshot", cascade="all, delete-orphan")


class IoTDeviceSensor(Base):
    """IoT Device Sensor model."""

    __tablename__ = "iot_device_sensors"

    sensor_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    iot_device_id: Mapped[UUID] = mapped_column(ForeignKey("iot_devices.iot_id",ondelete='CASCADE'), nullable=False)
    
    sensor_name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    iot_device:Mapped['IoTDevice'] = relationship("IoTDevice", back_populates="sensors")
    snapshot_sensor: Mapped[List['SensorSnapshot']] = relationship("SensorSnapshot", back_populates="iot_sensor_snapshot", cascade="all, delete-orphan")

class SensorSnapshot(Base):
    """Sensor Snapshot model."""

    __tablename__ = "sensor_snapshots"

    snapshots_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    iot_device_id: Mapped[UUID] = mapped_column(ForeignKey("iot_devices.iot_id", ondelete='CASCADE'), nullable=False)
    sensor_id: Mapped[UUID] = mapped_column(ForeignKey("iot_device_sensors.sensor_id", ondelete='CASCADE'), nullable=False)
    sensor_value: Mapped[float] = mapped_column(nullable=False)
    fuzzy_value: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    iot_device_snapshot: Mapped['IoTDevice'] = relationship("IoTDevice", back_populates="snapshot_device")
    iot_sensor_snapshot: Mapped['IoTDeviceSensor'] = relationship("IoTDeviceSensor", back_populates="snapshot_sensor")