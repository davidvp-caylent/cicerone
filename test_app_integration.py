"""
Integration test for AgentCore Runtime app.py

This script tests the basic functionality of the AgentCore integration
without requiring actual deployment to AWS.

Note: This test requires bedrock-agentcore to be installed:
    pip install bedrock-agentcore
"""

import sys
import os

# Check if bedrock-agentcore is installed
try:
    import bedrock_agentcore
except ImportError:
    print("⚠️  Warning: bedrock-agentcore is not installed")
    print("   To run these tests, install it with: pip install bedrock-agentcore")
    print("   Skipping integration tests...")
    sys.exit(0)

from unittest.mock import Mock, patch
from app import (
    _extract_user_message,
    _extract_session_id,
    _get_or_create_session,
    _update_session_history,
    _format_response
)


def test_extract_user_message():
    """Test message extraction from various payload formats."""
    print("Testing _extract_user_message...")
    
    # Test with 'prompt' key
    payload1 = {"prompt": "Hello"}
    assert _extract_user_message(payload1) == "Hello"
    
    # Test with 'message' key
    payload2 = {"message": "Hi there"}
    assert _extract_user_message(payload2) == "Hi there"
    
    # Test with 'input' key
    payload3 = {"input": "Test message"}
    assert _extract_user_message(payload3) == "Test message"
    
    # Test with missing message
    try:
        _extract_user_message({})
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "No user message found" in str(e)
    
    print("✓ _extract_user_message tests passed")


def test_extract_session_id():
    """Test session ID extraction and generation."""
    print("Testing _extract_session_id...")
    
    # Test with session_id
    payload1 = {"session_id": "test-123"}
    assert _extract_session_id(payload1) == "test-123"
    
    # Test with sessionId (camelCase)
    payload2 = {"sessionId": "test-456"}
    assert _extract_session_id(payload2) == "test-456"
    
    # Test with missing session_id (should generate new one)
    payload3 = {}
    session_id = _extract_session_id(payload3)
    assert len(session_id) > 0
    assert isinstance(session_id, str)
    
    print("✓ _extract_session_id tests passed")


def test_get_or_create_session():
    """Test session retrieval and creation."""
    print("Testing _get_or_create_session...")
    
    # Test creating new session
    session = _get_or_create_session("test-session-1", "user-123")
    assert session.session_id == "test-session-1"
    assert session.user_id == "user-123"
    assert len(session.beers_tasted) == 0
    assert len(session.conversation_history) == 0
    
    # Test retrieving existing session
    session2 = _get_or_create_session("test-session-1")
    assert session2.session_id == "test-session-1"
    assert session2.user_id == "user-123"  # Should preserve user_id
    
    print("✓ _get_or_create_session tests passed")


def test_update_session_history():
    """Test session history updates."""
    print("Testing _update_session_history...")
    
    session = _get_or_create_session("test-session-2")
    
    # Add first exchange
    _update_session_history(session, "Hello", "Hi there!")
    assert len(session.conversation_history) == 2
    assert session.conversation_history[0].role == "user"
    assert session.conversation_history[0].content == "Hello"
    assert session.conversation_history[1].role == "assistant"
    assert session.conversation_history[1].content == "Hi there!"
    
    # Add second exchange
    _update_session_history(session, "How are you?", "I'm doing well!")
    assert len(session.conversation_history) == 4
    
    print("✓ _update_session_history tests passed")


def test_format_response():
    """Test response formatting."""
    print("Testing _format_response...")
    
    # Test basic response
    response1 = _format_response("Test response", "session-123")
    assert response1["response"] == "Test response"
    assert response1["session_id"] == "session-123"
    assert response1["status"] == "success"
    
    # Test with metadata
    metadata = {"beers_tasted": 3, "has_profile": True}
    response2 = _format_response("Another response", "session-456", metadata)
    assert response2["metadata"] == metadata
    
    print("✓ _format_response tests passed")


def test_agent_invocation_error_handling():
    """Test error handling in agent invocation."""
    print("Testing agent_invocation error handling...")
    
    from app import agent_invocation
    
    # Test with invalid payload (missing message)
    payload = {}
    context = Mock()
    
    result = agent_invocation(payload, context)
    assert result["status"] == "error"
    assert "problema" in result["response"].lower()
    
    print("✓ agent_invocation error handling tests passed")


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("Running AgentCore Integration Tests")
    print("="*60 + "\n")
    
    try:
        test_extract_user_message()
        test_extract_session_id()
        test_get_or_create_session()
        test_update_session_history()
        test_format_response()
        test_agent_invocation_error_handling()
        
        print("\n" + "="*60)
        print("✓ All tests passed successfully!")
        print("="*60 + "\n")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
