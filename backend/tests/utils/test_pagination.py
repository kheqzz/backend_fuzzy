"""Test utility functions."""

import asyncio
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy import select
from app.utils.pagination import PaginationHelper


class TestPaginationHelper:
    """Tests for PaginationHelper."""

    def test_paginate_basic(self):
        from app.models.user import User
        mock_db = MagicMock()
        mock_db.scalar = AsyncMock(return_value=10)
        query = select(User)
        result = asyncio.run(
            PaginationHelper.paginate(mock_db, query, page=1, per_page=10)
        )
        assert result[1] == 10

    def test_get_pagination_header_basic(self):
        result = PaginationHelper.get_pagination_header(
            page=1, per_page=10, total_count=25
        )
        assert result["page"] == 1
        assert result["per_page"] == 10
        assert result["total_count"] == 25
        assert result["total_pages"] == 3
        assert result["has_previous"] is False
        assert result["has_next"] is True

    def test_get_pagination_header_exact_page(self):
        result = PaginationHelper.get_pagination_header(
            page=1, per_page=10, total_count=10
        )
        assert result["total_pages"] == 1
        assert result["has_next"] is False
        assert result["has_previous"] is False

    def test_get_pagination_header_last_page(self):
        result = PaginationHelper.get_pagination_header(
            page=3, per_page=10, total_count=25
        )
        assert result["page"] == 3
        assert result["has_previous"] is True
        assert result["has_next"] is False

    def test_get_pagination_header_first_page(self):
        result = PaginationHelper.get_pagination_header(
            page=1, per_page=10, total_count=100
        )
        assert result["has_previous"] is False
        assert result["has_next"] is True

    def test_get_pagination_header_single_item(self):
        result = PaginationHelper.get_pagination_header(
            page=1, per_page=10, total_count=1
        )
        assert result["total_pages"] == 1

    def test_get_pagination_header_zero_total(self):
        result = PaginationHelper.get_pagination_header(
            page=1, per_page=10, total_count=0
        )
        assert result["total_pages"] == 0
        assert result["has_next"] is False
