#!/usr/bin/env python3
"""Run all tests."""
import sys
import os
import pytest

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.exit(pytest.main(["tests/", "--tb=short", "-v"]))
