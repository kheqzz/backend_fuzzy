from uuid import UUID

from fastapi import HTTPException

"""Custom exception classes."""


class AppException(HTTPException):
    """Base exception for custom exceptions."""

    def __init__(self, message: str, status_code: int = 400, headers: dict | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(detail=message, status_code=status_code, headers=headers)


class EntityNotFoundError(AppException):
    """Raised when an entity is not found in the database."""

    def __init__(self, entity_name: str, entity_id: UUID):
        super().__init__(
            message=f"{entity_name} not found",
            status_code=404,
        )

class IoTNotFoundError(AppException):
    """Raised when an IoT device is not found in the database."""

    def __init__(self, entity_name: str, entity_id: UUID):
        super().__init__(
            message=f"{entity_name} not found",
            status_code=404,
        )

class UserNotFoundError(AppException):
    """Raised when a user is not found in the database."""

    def __init__(self, userLoginMethod: str):
        super().__init__(
            message=f"Invalid {userLoginMethod} or password",
            status_code=404,
        )
class EntityAlreadyExistsError(AppException):
    """Raised when an entity already exists (e.g., duplicate email)."""

    def __init__(self, entity_name: str, field: str, value: str):
        super().__init__(
            message=f"{entity_name} with {field} {value} already exists",
            status_code=409,
        )


class InvalidCredentialsError(AppException):
    """Raised when credentials are invalid."""

    def __init__(self):
        super().__init__(
            message="Could not validate credentials",
            status_code=401,
        )


class ForbiddenError(AppException):
    """Raised when the user does not have permission to perform an action."""

    def __init__(self, message: str = "Not enough permissions"):
        super().__init__(message=message, status_code=403)


class UnauthorizedError(AppException):
    """Raised when the user is not authenticated."""

    def __init__(self, message: str = "Not authenticated", headers: dict | None = None):
        super().__init__(message=message, status_code=401, headers=headers)