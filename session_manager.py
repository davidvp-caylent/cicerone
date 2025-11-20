"""Session management for Beer Tasting Agent.

This module provides in-memory session storage with automatic cleanup of old sessions.
Validates: Requirements 6.4, 8.1, 8.3
"""

from datetime import datetime, timedelta
from threading import Lock
from typing import Optional

from models.session import TastingSession


# In-memory session storage
_sessions: dict[str, TastingSession] = {}
_session_lock = Lock()

# Configuration
SESSION_TIMEOUT_HOURS = 24  # Sessions older than this will be cleaned up


def get_session_state(session_id: str) -> Optional[TastingSession]:
    """Retrieve session state by session ID.
    
    Args:
        session_id: Unique identifier for the session
        
    Returns:
        TastingSession object if found, None otherwise
        
    Validates: Requirements 8.1 - Session state retrieval
    """
    if not session_id or not isinstance(session_id, str):
        raise ValueError("Session ID must be a non-empty string")
    
    with _session_lock:
        # Clean up old sessions before retrieval
        _cleanup_old_sessions()
        
        return _sessions.get(session_id)


def save_session_state(session_id: str, session: TastingSession) -> None:
    """Save or update session state.
    
    Args:
        session_id: Unique identifier for the session
        session: TastingSession object to save
        
    Raises:
        ValueError: If session_id is invalid or session is not a TastingSession
        
    Validates: Requirements 8.1 - Session state persistence
    """
    if not session_id or not isinstance(session_id, str):
        raise ValueError("Session ID must be a non-empty string")
    
    if not isinstance(session, TastingSession):
        raise ValueError("Session must be a TastingSession object")
    
    if session.session_id != session_id:
        raise ValueError("Session ID mismatch: provided ID does not match session object ID")
    
    with _session_lock:
        _sessions[session_id] = session


def create_new_session(session_id: str, user_id: Optional[str] = None) -> TastingSession:
    """Create and save a new tasting session.
    
    Args:
        session_id: Unique identifier for the new session
        user_id: Optional user identifier
        
    Returns:
        Newly created TastingSession object
        
    Validates: Requirements 6.4 - New session initialization
    """
    if not session_id or not isinstance(session_id, str):
        raise ValueError("Session ID must be a non-empty string")
    
    session = TastingSession(
        session_id=session_id,
        user_id=user_id
    )
    
    save_session_state(session_id, session)
    return session


def delete_session(session_id: str) -> bool:
    """Delete a session from storage.
    
    Args:
        session_id: Unique identifier for the session to delete
        
    Returns:
        True if session was deleted, False if session didn't exist
    """
    if not session_id or not isinstance(session_id, str):
        raise ValueError("Session ID must be a non-empty string")
    
    with _session_lock:
        if session_id in _sessions:
            del _sessions[session_id]
            return True
        return False


def get_all_session_ids() -> list[str]:
    """Get list of all active session IDs.
    
    Returns:
        List of session IDs currently in storage
    """
    with _session_lock:
        return list(_sessions.keys())


def _cleanup_old_sessions() -> int:
    """Remove sessions older than SESSION_TIMEOUT_HOURS.
    
    This function is called automatically during get_session_state operations.
    
    Returns:
        Number of sessions cleaned up
        
    Validates: Requirements 8.3 - Automatic cleanup of old sessions
    """
    now = datetime.now()
    cutoff_time = now - timedelta(hours=SESSION_TIMEOUT_HOURS)
    
    sessions_to_remove = []
    
    for session_id, session in _sessions.items():
        if session.started_at < cutoff_time:
            sessions_to_remove.append(session_id)
    
    for session_id in sessions_to_remove:
        del _sessions[session_id]
    
    return len(sessions_to_remove)


def cleanup_old_sessions() -> int:
    """Manually trigger cleanup of old sessions.
    
    Returns:
        Number of sessions cleaned up
        
    Validates: Requirements 8.3 - Session cleanup
    """
    with _session_lock:
        return _cleanup_old_sessions()


def get_session_count() -> int:
    """Get the current number of active sessions.
    
    Returns:
        Number of sessions in storage
    """
    with _session_lock:
        return len(_sessions)
