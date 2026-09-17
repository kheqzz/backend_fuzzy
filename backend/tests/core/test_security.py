"""Test security module (password hashing, JWT tokens)."""

import pytest
from uuid import uuid4

from app.core.security import (
    get_password_hash,
    get_password_verify,
    create_access_token,
    decode_access_token,
    AuthError,
)
from app.core.config import settings
from app.core.exceptions import UnauthorizedError


class TestPasswordHashing:
    """Tests for password hashing and verification."""

    def test_password_hash_returns_string(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_password_hash_is_not_plaintext(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert hashed != password

    def test_password_verify_correct_password(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert get_password_verify(password, hashed) is True

    def test_password_verify_wrong_password(self):
        password = "correctpassword"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        assert get_password_verify(wrong_password, hashed) is False

    def test_password_verify_same_password_different_hashes(self):
        password = "testpassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2
        assert get_password_verify(password, hash1) is True
        assert get_password_verify(password, hash2) is True

    def test_password_verify_empty_string(self):
        hashed = get_password_hash("")
        assert get_password_verify("", hashed) is True


class TestCreateAccessToken:
    """Tests for JWT token creation."""

    def test_create_access_token_returns_string(self):
        token = create_access_token(secrets={"sub": str(uuid4())})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_custom_expiration(self):
        token = create_access_token(
            secrets={"sub": str(uuid4())},
            expiration_minutes=120,
        )
        assert isinstance(token, str)

    def test_create_access_token_payload_contains_sub(self):
        import jwt as pyjwt
        user_id = str(uuid4())
        token = create_access_token(secrets={"sub": user_id})
        decoded = pyjwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded["sub"] == user_id


class TestDecodeAccessToken:
    """Tests for JWT token decoding."""

    def test_decode_valid_token(self):
        user_id = uuid4()
        token = create_access_token(secrets={"sub": str(user_id)})
        decoded = decode_access_token(token)
        assert decoded == user_id

    def test_decode_invalid_token_raises_error(self):
        with pytest.raises(UnauthorizedError):
            decode_access_token("invalid.token.here")

    def test_decode_expired_token_raises_error(self):
        import jwt as pyjwt
        import datetime
        expired_payload = {
            "sub": str(uuid4()),
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            - datetime.timedelta(hours=1),
        }
        expired_token = pyjwt.encode(
            expired_payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        with pytest.raises(UnauthorizedError):
            decode_access_token(expired_token)

    def test_decode_token_without_sub_raises_error(self):
        import jwt as pyjwt
        payload = {"other": "data"}
        token = pyjwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        with pytest.raises(UnauthorizedError):
            decode_access_token(token)

    def test_decode_empty_token_raises_error(self):
        with pytest.raises(UnauthorizedError):
            decode_access_token("")


class TestAuthError:
    """Tests for AuthError base class."""

    def test_auth_error_basic(self):
        exc = AuthError("Test auth error")
        assert str(exc) == "Test auth error"
        assert exc.status_code == 401

    def test_auth_error_custom_status_code(self):
        exc = AuthError("Auth error", status_code=403)
        assert exc.status_code == 403
