"""
Pytest configuration and shared fixtures for Beer Tasting Agent tests.
"""
import pytest
from hypothesis import settings, Verbosity

# Configure Hypothesis for all property-based tests
settings.register_profile("default", max_examples=100, deadline=None)
settings.register_profile("ci", max_examples=200, deadline=None)
settings.register_profile("dev", max_examples=50, deadline=None, verbosity=Verbosity.verbose)

# Load the default profile
settings.load_profile("default")


@pytest.fixture
def sample_beer_data():
    """Fixture providing sample beer data for testing."""
    return {
        "id": "test-beer-1",
        "name": "Test IPA",
        "style": "American IPA",
        "abv": 6.5,
        "ibu": 65,
        "description": "A hoppy American IPA with citrus notes"
    }


@pytest.fixture
def sample_preference_profile():
    """Fixture providing sample preference profile for testing."""
    return {
        "preferred_styles": ["IPA", "Pale Ale"],
        "bitterness_preference": "high",
        "alcohol_tolerance": "moderate",
        "flavor_notes": ["citrus", "pine", "tropical"],
        "body_preference": "medium"
    }


@pytest.fixture
def sample_session_data():
    """Fixture providing sample session data for testing."""
    return {
        "session_id": "test-session-123",
        "beers_tasted": ["beer-1", "beer-2"],
        "evaluations": {},
        "preference_profile": None
    }
