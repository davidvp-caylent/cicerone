"""
Basic setup test to verify the testing infrastructure is working.
"""
import pytest


def test_pytest_working():
    """Verify that pytest is properly configured."""
    assert True


def test_imports():
    """Verify that basic Python imports work."""
    import sys
    import os
    assert sys.version_info >= (3, 9)


@pytest.mark.unit
def test_fixtures_available(sample_beer_data):
    """Verify that shared fixtures from conftest.py are available."""
    assert sample_beer_data is not None
    assert "id" in sample_beer_data
    assert "name" in sample_beer_data
