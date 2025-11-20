"""Tests for data models."""

import pytest
from datetime import datetime
from models import (
    Beer,
    BeerDetails,
    PreferenceProfile,
    TastingSession,
    BeerEvaluation,
    Message,
)


class TestBeer:
    """Tests for Beer model."""
    
    def test_valid_beer_creation(self):
        """Test creating a valid beer."""
        beer = Beer(
            id="1",
            name="Test IPA",
            style="IPA",
            abv=6.5,
            ibu=60,
            description="A hoppy IPA"
        )
        assert beer.name == "Test IPA"
        assert beer.abv == 6.5
    
    def test_beer_requires_name(self):
        """Test that beer requires a name."""
        with pytest.raises(ValueError, match="name must be a non-empty string"):
            Beer(
                id="1",
                name="",
                style="IPA",
                abv=6.5,
                ibu=60,
                description="A hoppy IPA"
            )
    
    def test_beer_validates_abv_range(self):
        """Test that ABV is validated."""
        with pytest.raises(ValueError, match="ABV must be a number between 0 and 20"):
            Beer(
                id="1",
                name="Test Beer",
                style="IPA",
                abv=25.0,
                ibu=60,
                description="Invalid ABV"
            )


class TestBeerDetails:
    """Tests for BeerDetails model."""
    
    def test_valid_beer_details_creation(self):
        """Test creating valid beer details."""
        beer = Beer(
            id="1",
            name="Test IPA",
            style="IPA",
            abv=6.5,
            ibu=60,
            description="A hoppy IPA"
        )
        details = BeerDetails(
            beer=beer,
            tasting_notes="Citrus and pine",
            ingredients="Hops, malt, yeast, water"
        )
        assert details.beer.name == "Test IPA"
        assert details.tasting_notes == "Citrus and pine"


class TestPreferenceProfile:
    """Tests for PreferenceProfile model."""
    
    def test_valid_preference_profile_creation(self):
        """Test creating a valid preference profile."""
        profile = PreferenceProfile(
            preferred_styles=["IPA", "Stout"],
            bitterness_preference="high",
            alcohol_tolerance="moderate",
            flavor_notes=["citrus", "coffee"],
            body_preference="full"
        )
        assert profile.preferred_styles == ["IPA", "Stout"]
        assert profile.bitterness_preference == "high"
    
    def test_preference_profile_validates_bitterness(self):
        """Test that bitterness preference is validated."""
        with pytest.raises(ValueError, match="Bitterness preference must be one of"):
            PreferenceProfile(bitterness_preference="invalid")


class TestMessage:
    """Tests for Message model."""
    
    def test_valid_message_creation(self):
        """Test creating a valid message."""
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert isinstance(msg.timestamp, datetime)
    
    def test_message_validates_role(self):
        """Test that message role is validated."""
        with pytest.raises(ValueError, match="role must be one of"):
            Message(role="invalid", content="Hello")


class TestBeerEvaluation:
    """Tests for BeerEvaluation model."""
    
    def test_valid_beer_evaluation_creation(self):
        """Test creating a valid beer evaluation."""
        eval = BeerEvaluation(
            beer_id="1",
            appearance_notes="Golden color",
            aroma_notes="Hoppy",
            taste_notes="Bitter and citrusy",
            mouthfeel_notes="Medium body",
            overall_rating=4
        )
        assert eval.beer_id == "1"
        assert eval.overall_rating == 4
    
    def test_beer_evaluation_validates_rating(self):
        """Test that rating is validated."""
        with pytest.raises(ValueError, match="rating must be an integer between 1 and 5"):
            BeerEvaluation(beer_id="1", overall_rating=6)


class TestTastingSession:
    """Tests for TastingSession model."""
    
    def test_valid_tasting_session_creation(self):
        """Test creating a valid tasting session."""
        session = TastingSession(
            session_id="session-1",
            user_id="user-1"
        )
        assert session.session_id == "session-1"
        assert session.user_id == "user-1"
        assert isinstance(session.started_at, datetime)
        assert session.beers_tasted == []
        assert session.evaluations == {}
    
    def test_tasting_session_with_evaluations(self):
        """Test tasting session with evaluations."""
        eval1 = BeerEvaluation(beer_id="1", overall_rating=4)
        session = TastingSession(
            session_id="session-1",
            beers_tasted=["1"],
            evaluations={"1": eval1}
        )
        assert len(session.evaluations) == 1
        assert session.evaluations["1"].beer_id == "1"
