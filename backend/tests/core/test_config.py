"""Test configuration settings."""

import pytest
from app.core.config import Settings, settings


class TestSettingsDefaults:
    """Tests for default settings values."""

    def test_project_name_default(self):
        assert Settings().PROJECT_NAME == "FastAPI Project"

    def test_api_v1_prefix_default(self):
        assert Settings().API_V1_PREFIX == "/api/v1"

    def test_backend_cors_origins_default(self):
        assert Settings().BACKEND_CORS_ORIGINS == []

    def test_algorithm_default(self):
        assert Settings().ALGORITHM == "HS256"

    def test_access_token_expire_minutes_default(self):
        assert Settings().ACCESS_TOKEN_EXPIRE_MINUTES == 30


class TestSettingsFromEnv:
    """Tests for settings loaded from environment."""

    def test_settings_is_instance_of_settings(self):
        assert isinstance(settings, Settings)

    def test_settings_has_required_attributes(self):
        assert hasattr(settings, "DATABASE_URL")
        assert hasattr(settings, "SECRET_KEY")
        assert hasattr(settings, "PROJECT_NAME")

    def test_settings_database_url_is_string(self):
        assert isinstance(settings.DATABASE_URL, str)

    def test_settings_secret_key_is_string(self):
        assert isinstance(settings.SECRET_KEY, str)

    def test_settings_algorithm(self):
        assert settings.ALGORITHM in ("HS256", "HS384", "HS512")


class TestSettingsExtraIgnore:
    """Test that extra fields are ignored."""

    def test_extra_fields_ignored(self):
        s = Settings(extra_field="should_be_ignored")
        assert not hasattr(s, "extra_field")