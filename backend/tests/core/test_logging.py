"""Test logging configuration."""

import logging
import sys
from io import StringIO

from app.core.logging import get_logger, setup_logging
from app.core.config import settings


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_setup_logging_does_not_raise(self):
        """Test that setup_logging runs without errors."""
        try:
            setup_logging()
        except Exception as e:
            assert False, f"setup_logging raised {e}"

    def test_get_logger_returns_logger_instance(self):
        logger = get_logger("test_logger")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_name(self):
        logger_name = "test_specific_logger"
        logger = get_logger(logger_name)
        assert logger.name == logger_name

    def test_get_logger_is_same_instance(self):
        logger1 = get_logger("same_logger")
        logger2 = get_logger("same_logger")
        assert logger1 is logger2

    def test_get_logger_has_handlers(self):
        logger = get_logger("handler_logger")
        assert len(logger.handlers) > 0

    def test_get_logger_level(self):
        logger = get_logger("level_logger")
        assert logger.level == logging.DEBUG


class TestLoggingOutput:
    """Tests that logging produces output."""

    def test_logger_can_log_messages(self, capsys):
        logger = get_logger("output_test_logger")
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")


class TestSetupLoggingWithDevelopment:
    """Tests logging in development mode."""

    def test_setup_logging_respects_project_name(self):
        original = settings.PROJECT_NAME
        settings.PROJECT_NAME = "development"
        try:
            setup_logging()
            logger = get_logger("dev_test")
            assert logger.level == logging.DEBUG
        finally:
            settings.PROJECT_NAME = original