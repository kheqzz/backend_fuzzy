"""Shared test fixtures and configuration."""

import asyncio
import os
import sys
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Ensure app directory is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

_test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
_test_session_factory = async_sessionmaker(
    _test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = _test_session_factory()
    try:
        yield session
    finally:
        await session.close()
        async with _test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Alias for db_session."""
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = _test_session_factory()
    try:
        yield session
    finally:
        await session.close()
        async with _test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def sample_user_data():
    """Sample user data for tests."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
    }


@pytest.fixture
def sample_device_data():
    """Sample IoT device data for tests."""
    return {
        "name": "Test Device",
        "description": "A test IoT device",
        "iot_firmware_version": "1.0.0",
    }


@pytest.fixture
def sample_sensor_data():
    """Sample IoT sensor data for tests."""
    return {
        "sensor_name": "Temperature",
        "unit": "Celsius",
    }


@pytest.fixture
def sample_snapshot_data():
    """Sample sensor snapshot data for tests."""
    return {
        "sensor_value": 25.5,
        "fuzzy_value": "medium",
    }
