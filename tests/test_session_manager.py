"""Tests for session manager."""

import pytest
from datetime import datetime, timedelta
from models import TastingSession, PreferenceProfile, BeerEvaluation
import session_manager


class TestSessionManager:
    """Tests for session management functions."""
    
    def setup_method(self):
        """Clear sessions before each test."""
        # Clear all sessions
        for session_id in session_manager.get_all_session_ids():
            session_manager.delete_session(session_id)
    
    def test_create_new_session(self):
        """Test creating a new session."""
        session = session_manager.create_new_session("test-session-1", "user-1")
        
        assert session.session_id == "test-session-1"
        assert session.user_id == "user-1"
        assert isinstance(session.started_at, datetime)
        assert session.beers_tasted == []
        assert session.evaluations == {}
    
    def test_save_and_retrieve_session(self):
        """Test saving and retrieving a session."""
        session = TastingSession(
            session_id="test-session-2",
            user_id="user-2",
            beers_tasted=["beer-1", "beer-2"]
        )
        
        session_manager.save_session_state("test-session-2", session)
        retrieved = session_manager.get_session_state("test-session-2")
        
        assert retrieved is not None
        assert retrieved.session_id == "test-session-2"
        assert retrieved.user_id == "user-2"
        assert retrieved.beers_tasted == ["beer-1", "beer-2"]
    
    def test_get_nonexistent_session(self):
        """Test retrieving a session that doesn't exist."""
        result = session_manager.get_session_state("nonexistent")
        assert result is None
    
    def test_update_existing_session(self):
        """Test updating an existing session."""
        session = session_manager.create_new_session("test-session-3")
        
        # Update the session
        session.beers_tasted.append("beer-1")
        session_manager.save_session_state("test-session-3", session)
        
        # Retrieve and verify
        retrieved = session_manager.get_session_state("test-session-3")
        assert retrieved.beers_tasted == ["beer-1"]
    
    def test_delete_session(self):
        """Test deleting a session."""
        session_manager.create_new_session("test-session-4")
        
        # Verify it exists
        assert session_manager.get_session_state("test-session-4") is not None
        
        # Delete it
        result = session_manager.delete_session("test-session-4")
        assert result is True
        
        # Verify it's gone
        assert session_manager.get_session_state("test-session-4") is None
    
    def test_delete_nonexistent_session(self):
        """Test deleting a session that doesn't exist."""
        result = session_manager.delete_session("nonexistent")
        assert result is False
    
    def test_get_all_session_ids(self):
        """Test getting all session IDs."""
        session_manager.create_new_session("session-1")
        session_manager.create_new_session("session-2")
        session_manager.create_new_session("session-3")
        
        session_ids = session_manager.get_all_session_ids()
        assert len(session_ids) == 3
        assert "session-1" in session_ids
        assert "session-2" in session_ids
        assert "session-3" in session_ids
    
    def test_get_session_count(self):
        """Test getting session count."""
        initial_count = session_manager.get_session_count()
        
        session_manager.create_new_session("count-test-1")
        session_manager.create_new_session("count-test-2")
        
        assert session_manager.get_session_count() == initial_count + 2
    
    def test_session_id_mismatch_raises_error(self):
        """Test that mismatched session IDs raise an error."""
        session = TastingSession(session_id="session-a")
        
        with pytest.raises(ValueError, match="Session ID mismatch"):
            session_manager.save_session_state("session-b", session)
    
    def test_invalid_session_id_raises_error(self):
        """Test that invalid session IDs raise errors."""
        with pytest.raises(ValueError, match="Session ID must be a non-empty string"):
            session_manager.get_session_state("")
        
        with pytest.raises(ValueError, match="Session ID must be a non-empty string"):
            session_manager.create_new_session("")
    
    def test_invalid_session_object_raises_error(self):
        """Test that invalid session objects raise errors."""
        with pytest.raises(ValueError, match="Session must be a TastingSession object"):
            session_manager.save_session_state("test", "not a session")
    
    def test_cleanup_old_sessions(self):
        """Test automatic cleanup of old sessions."""
        # Create a session with an old timestamp
        old_session = TastingSession(session_id="old-session")
        old_session.started_at = datetime.now() - timedelta(hours=25)
        session_manager.save_session_state("old-session", old_session)
        
        # Create a recent session
        session_manager.create_new_session("recent-session")
        
        # Trigger cleanup
        cleaned = session_manager.cleanup_old_sessions()
        
        # Old session should be removed
        assert session_manager.get_session_state("old-session") is None
        # Recent session should still exist
        assert session_manager.get_session_state("recent-session") is not None
        assert cleaned == 1
    
    def test_cleanup_triggered_on_get(self):
        """Test that cleanup is triggered automatically on get_session_state."""
        # Create an old session
        old_session = TastingSession(session_id="auto-cleanup-test")
        old_session.started_at = datetime.now() - timedelta(hours=26)
        session_manager.save_session_state("auto-cleanup-test", old_session)
        
        # Getting any session should trigger cleanup
        session_manager.get_session_state("some-other-session")
        
        # Old session should be cleaned up
        assert session_manager.get_session_state("auto-cleanup-test") is None
    
    def test_session_with_preference_profile(self):
        """Test session with preference profile."""
        profile = PreferenceProfile(
            preferred_styles=["IPA"],
            bitterness_preference="high"
        )
        session = TastingSession(
            session_id="profile-test",
            preference_profile=profile
        )
        
        session_manager.save_session_state("profile-test", session)
        retrieved = session_manager.get_session_state("profile-test")
        
        assert retrieved.preference_profile is not None
        assert retrieved.preference_profile.preferred_styles == ["IPA"]
        assert retrieved.preference_profile.bitterness_preference == "high"
    
    def test_session_with_evaluations(self):
        """Test session with beer evaluations."""
        eval1 = BeerEvaluation(beer_id="beer-1", overall_rating=5)
        eval2 = BeerEvaluation(beer_id="beer-2", overall_rating=3)
        
        session = TastingSession(
            session_id="eval-test",
            beers_tasted=["beer-1", "beer-2"],
            evaluations={"beer-1": eval1, "beer-2": eval2}
        )
        
        session_manager.save_session_state("eval-test", session)
        retrieved = session_manager.get_session_state("eval-test")
        
        assert len(retrieved.evaluations) == 2
        assert retrieved.evaluations["beer-1"].overall_rating == 5
        assert retrieved.evaluations["beer-2"].overall_rating == 3
