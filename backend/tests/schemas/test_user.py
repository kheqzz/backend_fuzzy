"""Test user schemas."""

import pytest
from uuid import uuid4
from pydantic import ValidationError
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserOut,
    UserUpdate,
    UserLogin,
    TokenResponse,
)


class TestUserBase:
    """Tests for UserBase schema."""

    def test_user_base_valid(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
        }
        schema = UserBase(**data)
        assert schema.username == "testuser"
        assert schema.email == "test@example.com"
        assert schema.full_name == "Test User"

    def test_user_base_username_required(self):
        with pytest.raises(ValidationError):
            UserBase(email="test@example.com", full_name="Test")

    def test_user_base_email_required(self):
        with pytest.raises(ValidationError):
            UserBase(username="testuser", full_name="Test")

    def test_user_base_full_name_required(self):
        with pytest.raises(ValidationError):
            UserBase(username="testuser", email="test@example.com")


class TestUserCreate:
    """Tests for UserCreate schema."""

    def test_user_create_valid(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "full_name": "New User",
            "password": "securepassword123",
        }
        schema = UserCreate(**data)
        assert schema.username == "newuser"
        assert schema.password == "securepassword123"

    def test_user_create_password_required(self):
        with pytest.raises(ValidationError):
            UserCreate(username="user", email="test@example.com", full_name="User")


class TestUserOut:
    """Tests for UserOut schema."""

    def test_user_out_valid(self):
        data = {
            "id": uuid4(),
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "is_superuser": False,
        }
        schema = UserOut(**data)
        assert schema.id == data["id"]
        assert schema.is_active is True
        assert schema.is_superuser is False

    def test_user_out_from_attributes(self):
        class FakeUser:
            id = uuid4()
            username = "fakeuser"
            email = "fake@example.com"
            full_name = "Fake User"
            is_active = True
            is_superuser = False

        schema = UserOut.model_validate(FakeUser())
        assert schema.id is not None
        assert schema.username == "fakeuser"


class TestUserUpdate:
    """Tests for UserUpdate schema."""

    def test_user_update_all_fields(self):
        data = {
            "username": "updated",
            "email": "updated@example.com",
            "full_name": "Updated User",
            "password": "newpass123",
            "is_active": False,
            "is_superuser": True,
        }
        schema = UserUpdate(**data)
        assert schema.username == "updated"

    def test_user_update_partial(self):
        schema = UserUpdate(username="newname")
        assert schema.username == "newname"
        assert schema.email is None
        assert schema.full_name is None

    def test_user_update_only_username(self):
        schema = UserUpdate()
        assert schema.username is None


class TestUserLogin:
    """Tests for UserLogin schema."""

    def test_user_login_valid(self):
        data = {"username": "testuser", "password": "testpass"}
        schema = UserLogin(**data)
        assert schema.username == "testuser"
        assert schema.password == "testpass"

    def test_user_login_username_required(self):
        with pytest.raises(ValidationError):
            UserLogin(password="testpass")


class TestTokenResponse:
    """Tests for TokenResponse schema."""

    def test_token_response_valid(self):
        from app.schemas.user import UserOut
        data = {
            "access_token": "test_token_123",
            "token_type": "bearer",
            "user": UserOut(
                id=uuid4(),
                username="testuser",
                email="test@example.com",
                full_name="Test User",
                is_active=True,
                is_superuser=False,
            ),
        }
        schema = TokenResponse(**data)
        assert schema.access_token == "test_token_123"
        assert schema.token_type == "bearer"
        assert schema.user.username == "testuser"

    def test_token_response_default_token_type(self):
        from app.schemas.user import UserOut
        schema = TokenResponse(
            access_token="token",
            user=UserOut(
                id=uuid4(),
                username="test",
                email="test@test.com",
                full_name="Test",
                is_active=True,
                is_superuser=False,
            ),
        )
        assert schema.token_type == "bearer"
