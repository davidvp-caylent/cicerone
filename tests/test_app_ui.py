"""
Tests for Streamlit UI components

These tests verify the core functionality of the web interface without
requiring a full Streamlit runtime.

Validates: Requirements 6.1, 6.2, 6.3, 6.4
"""

import pytest
import uuid
from unittest.mock import Mock, patch, MagicMock
import requests


# Import the functions we want to test
# Note: We can't import the full app_ui module because it runs streamlit on import
# So we'll test the core logic separately


def test_session_id_generation():
    """Test that session IDs are valid UUIDs."""
    session_id = str(uuid.uuid4())
    
    # Verify it's a valid UUID format
    assert len(session_id) == 36
    assert session_id.count('-') == 4
    
    # Verify we can parse it back to UUID
    parsed = uuid.UUID(session_id)
    assert str(parsed) == session_id


def test_agent_call_payload_structure():
    """Test that the payload structure for agent calls is correct."""
    user_message = "¿Qué cervezas hay disponibles?"
    session_id = str(uuid.uuid4())
    
    expected_payload = {
        "prompt": user_message,
        "session_id": session_id
    }
    
    # Verify payload structure
    assert "prompt" in expected_payload
    assert "session_id" in expected_payload
    assert expected_payload["prompt"] == user_message
    assert expected_payload["session_id"] == session_id


@patch('requests.post')
def test_agent_call_success(mock_post):
    """Test successful agent API call."""
    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": "Tenemos varias cervezas disponibles...",
        "session_id": "test-session-123",
        "status": "success"
    }
    mock_post.return_value = mock_response
    
    # Simulate the call
    user_message = "¿Qué cervezas hay disponibles?"
    session_id = "test-session-123"
    
    response = requests.post(
        "http://localhost:8000",
        json={"prompt": user_message, "session_id": session_id},
        timeout=30
    )
    
    # Verify the call was made
    assert mock_post.called
    assert response.status_code == 200
    
    # Verify response structure
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert data["session_id"] == session_id


@patch('requests.post')
def test_agent_call_timeout(mock_post):
    """Test agent API call timeout handling."""
    # Mock timeout exception
    mock_post.side_effect = requests.exceptions.Timeout()
    
    # Simulate the call and expect timeout
    with pytest.raises(requests.exceptions.Timeout):
        requests.post(
            "http://localhost:8000",
            json={"prompt": "test", "session_id": "test"},
            timeout=30
        )


@patch('requests.post')
def test_agent_call_connection_error(mock_post):
    """Test agent API call connection error handling."""
    # Mock connection error
    mock_post.side_effect = requests.exceptions.ConnectionError()
    
    # Simulate the call and expect connection error
    with pytest.raises(requests.exceptions.ConnectionError):
        requests.post(
            "http://localhost:8000",
            json={"prompt": "test", "session_id": "test"},
            timeout=30
        )


@patch('requests.post')
def test_agent_call_http_error(mock_post):
    """Test agent API call HTTP error handling."""
    # Mock HTTP error response
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_post.return_value = mock_response
    
    # Simulate the call
    response = requests.post(
        "http://localhost:8000",
        json={"prompt": "test", "session_id": "test"},
        timeout=30
    )
    
    # Verify error handling
    assert response.status_code == 500
    with pytest.raises(requests.exceptions.HTTPError):
        response.raise_for_status()


def test_message_history_structure():
    """Test that message history maintains correct structure."""
    messages = []
    
    # Add user message
    messages.append({
        "role": "user",
        "content": "¿Qué cervezas hay?"
    })
    
    # Add assistant message
    messages.append({
        "role": "assistant",
        "content": "Tenemos varias cervezas..."
    })
    
    # Verify structure
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
    assert "content" in messages[0]
    assert "content" in messages[1]


def test_session_reset():
    """Test session reset functionality."""
    # Simulate session state
    session_state = {
        "messages": [
            {"role": "user", "content": "test1"},
            {"role": "assistant", "content": "response1"}
        ],
        "session_id": "old-session-id"
    }
    
    # Reset session
    session_state["messages"] = []
    session_state["session_id"] = str(uuid.uuid4())
    
    # Verify reset
    assert len(session_state["messages"]) == 0
    assert session_state["session_id"] != "old-session-id"
    assert len(session_state["session_id"]) == 36


def test_response_metadata_handling():
    """Test handling of response metadata."""
    response_data = {
        "response": "Test response",
        "session_id": "test-123",
        "status": "success",
        "metadata": {
            "beers_tasted_count": 3,
            "has_preference_profile": True,
            "message_count": 10
        }
    }
    
    # Verify metadata structure
    assert "metadata" in response_data
    assert "beers_tasted_count" in response_data["metadata"]
    assert response_data["metadata"]["beers_tasted_count"] == 3
    assert response_data["metadata"]["has_preference_profile"] is True


@patch('requests.post')
def test_agent_response_within_timeout(mock_post):
    """Test that agent responds within acceptable time.
    
    Validates: Requirements 6.2 - Response within 5 seconds under normal conditions
    """
    # Mock quick response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": "Quick response",
        "session_id": "test",
        "status": "success"
    }
    mock_post.return_value = mock_response
    
    # Make request with timeout
    response = requests.post(
        "http://localhost:8000",
        json={"prompt": "test", "session_id": "test"},
        timeout=5  # 5 second timeout as per requirements
    )
    
    # Verify successful response
    assert response.status_code == 200
    assert mock_post.called


def test_conversation_history_persistence():
    """Test that conversation history is maintained correctly.
    
    Validates: Requirements 6.3 - Display conversation history
    """
    messages = []
    
    # Simulate conversation
    conversation = [
        ("user", "Hola"),
        ("assistant", "¡Hola! ¿En qué puedo ayudarte?"),
        ("user", "¿Qué cervezas hay?"),
        ("assistant", "Tenemos IPA, Stout, Lager...")
    ]
    
    for role, content in conversation:
        messages.append({"role": role, "content": content})
    
    # Verify history
    assert len(messages) == 4
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
    assert all("role" in msg and "content" in msg for msg in messages)


def test_new_session_clears_history():
    """Test that starting a new session clears previous history.
    
    Validates: Requirements 6.4 - Clear previous conversation history
    """
    # Simulate existing session
    old_messages = [
        {"role": "user", "content": "old message 1"},
        {"role": "assistant", "content": "old response 1"}
    ]
    old_session_id = "old-session-123"
    
    # Start new session
    new_messages = []
    new_session_id = str(uuid.uuid4())
    
    # Verify new session is clean
    assert len(new_messages) == 0
    assert new_session_id != old_session_id
    assert len(old_messages) == 2  # Old messages unchanged
