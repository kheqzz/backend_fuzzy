"""Test custom exceptions."""

import pytest
from uuid import uuid4

from app.core.exceptions import (
    AppException,
    EntityNotFoundError,
    IoTNotFoundError,
    UserNotFoundError,
    EntityAlreadyExistsError,
    InvalidCredentialsError,
    ForbiddenError,
    UnauthorizedError,
)


class TestAppException:
    """Tests for AppException base class."""

    def test_app_exception_returns_correct_status_code(self):
        exc = AppException(message="Test error", status_code=400)
        assert exc.status_code == 400
        assert exc.message == "Test error"
        assert exc.detail == "Test error"

    def test_app_exception_default_status_code(self):
        exc = AppException(message="Default error")
        assert exc.status_code == 400


class TestEntityNotFoundError:
    """Tests for EntityNotFoundError."""

    def test_entity_not_found_error(self):
        entity_id = uuid4()
        exc = EntityNotFoundError(entity_name="User", entity_id=entity_id)
        assert exc.status_code == 404
        assert exc.message == "User not found"
        assert exc.detail == "User not found"

    def test_entity_not_found_error_with_different_entity(self):
        exc = EntityNotFoundError(entity_name="IoTDevice", entity_id=uuid4())
        assert exc.status_code == 404
        assert "IoTDevice" in exc.message


class TestIoTNotFoundError:
    """Tests for IoTNotFoundError."""

    def test_iot_not_found_error(self):
        exc = IoTNotFoundError(entity_name="IoTDevice", entity_id=uuid4())
        assert exc.status_code == 404
        assert "IoTDevice" in exc.message


class TestUserNotFoundError:
    """Tests for UserNotFoundError."""

    def test_user_not_found_error(self):
        exc = UserNotFoundError(userLoginMethod="username")
        assert exc.status_code == 404
        assert "username" in exc.message
        assert "password" in exc.message


class TestEntityAlreadyExistsError:
    """Tests for EntityAlreadyExistsError."""

    def test_entity_already_exists_error(self):
        exc = EntityAlreadyExistsError("User", "email", "test@example.com")
        assert exc.status_code == 409
        assert "User" in exc.message
        assert "email" in exc.message
        assert "test@example.com" in exc.message


class TestInvalidCredentialsError:
    """Tests for InvalidCredentialsError."""

    def test_invalid_credentials_error(self):
        exc = InvalidCredentialsError()
        assert exc.status_code == 401
        assert exc.message == "Could not validate credentials"


class TestForbiddenError:
    """Tests for ForbiddenError."""

    def test_forbidden_error_default_message(self):
        exc = ForbiddenError()
        assert exc.status_code == 403
        assert exc.message == "Not enough permissions"

    def test_forbidden_error_custom_message(self):
        exc = ForbiddenError(message="Access denied")
        assert exc.status_code == 403
        assert exc.message == "Access denied"


class TestUnauthorizedError:
    """Tests for UnauthorizedError."""

    def test_unauthorized_error_default(self):
        exc = UnauthorizedError()
        assert exc.status_code == 401
        assert exc.message == "Not authenticated"
        assert exc.headers is None

    def test_unauthorized_error_with_message(self):
        exc = UnauthorizedError(message="Token expired")
        assert exc.status_code == 401
        assert exc.message == "Token expired"

    def test_unauthorized_error_with_headers(self):
        headers = {"WWW-Authenticate": "Bearer"}
        exc = UnauthorizedError(message="Invalid token", headers=headers)
        assert exc.headers == headers