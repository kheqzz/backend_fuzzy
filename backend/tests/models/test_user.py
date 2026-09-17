"""Test User model."""

import pytest
from datetime import datetime
from uuid import uuid4
from sqlalchemy import select
from app.models.user import User
from app.db.base import Base
import sqlalchemy as sa
from uuid import UUID


class TestUserModel:
    """Tests for User model."""

    @pytest.mark.asyncio
    async def test_user_has_id(self, db):
        user = User(id=uuid4(), username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        assert user.id is not None

    @pytest.mark.asyncio
    async def test_user_default_values(self, db):
        user = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        assert user.is_active is True
        assert user.is_superuser is False
        assert user.created_at is not None
        assert user.updated_at is not None

    @pytest.mark.asyncio
    async def test_user_unique_username(self, db):
        user1 = User(username="testuser", email="test1@test.com", full_name="User 1", hashed_password="dummy")
        db.add(user1)
        await db.commit()
        await db.refresh(user1)
        # Trying to add duplicate username should fail
        user2 = User(username="testuser", email="test2@test.com", full_name="User 2", hashed_password="dummy")
        db.add(user2)
        with pytest.raises(Exception):
            await db.commit()
        # Clean up
        await db.rollback()

    @pytest.mark.asyncio
    async def test_user_unique_email(self, db):
        user1 = User(username="user1", email="test@test.com", full_name="User 1", hashed_password="dummy")
        db.add(user1)
        await db.commit()
        await db.refresh(user1)
        # Trying to add duplicate email should fail
        user2 = User(username="user2", email="test@test.com", full_name="User 2", hashed_password="dummy")
        db.add(user2)
        with pytest.raises(Exception):
            await db.commit()
        await db.rollback()

    @pytest.mark.asyncio
    async def test_user_relationship_with_iot_devices(self, db):
        from app.models.iot import IoTDevice
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
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
        # Use selectinload to properly load the relationship in async mode
        result = (await db.execute(
            select(User).options(selectinload(User.iot_devices)).where(User.id == user.id)
        )).scalars().first()
        assert len(result.iot_devices) == 1
        assert result.iot_devices[0].name == "Device 1"

    @pytest.mark.asyncio
    async def test_user_cascade_delete_user(self, db):
        from app.models.iot import IoTDevice
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

    def test_user_has_required_fields(self):
        user = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        assert user.username == "test"
        assert user.email == "test@test.com"
        assert user.full_name == "Test"

    def test_user_is_active_default_true(self):
        user = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        # SQLAlchemy defaults are applied on flush, so we need to trigger that
        # by using the column's default
        from app.models.user import User as UserModel
        col = UserModel.__table__.c.is_active
        default = col.default
        if callable(default):
            assert default() is True
        else:
            assert default.arg is True

    def test_user_is_superuser_default_false(self):
        user = User(username="test", email="test@test.com", full_name="Test", hashed_password="dummy")
        # SQLAlchemy defaults are applied on flush, so we check the column default
        from app.models.user import User as UserModel
        col = UserModel.__table__.c.is_superuser
        default = col.default
        if callable(default):
            assert default() is False
        else:
            assert default.arg is False