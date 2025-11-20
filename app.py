"""
Beer Tasting Agent - AgentCore Runtime Integration

This module integrates the Beer Tasting Agent with Amazon Bedrock AgentCore Runtime,
providing a serverless deployment with session management and error handling.

Validates: Requirements 7.1, 7.3
"""

import os
import logging
import uuid
from typing import Any, Dict, Optional

from bedrock_agentcore import BedrockAgentCoreApp
from agent import agent
from session_manager import (
    get_session_state,
    save_session_state,
    create_new_session
)
from models.session import TastingSession, Message

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize AgentCore application
app = BedrockAgentCoreApp()

# Environment configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'us.anthropic.claude-sonnet-4-5-20250929-v1:0')


def _extract_user_message(payload: Dict[str, Any]) -> str:
    """Extract user message from payload.
    
    Args:
        payload: Request payload from AgentCore
        
    Returns:
        User message string
        
    Raises:
        ValueError: If message cannot be extracted
    """
    # Try different payload formats
    message = payload.get('prompt') or payload.get('message') or payload.get('input')
    
    if not message:
        raise ValueError("No user message found in payload")
    
    if not isinstance(message, str):
        raise ValueError("User message must be a string")
    
    return message


def _extract_session_id(payload: Dict[str, Any]) -> str:
    """Extract or generate session ID from payload.
    
    Args:
        payload: Request payload from AgentCore
        
    Returns:
        Session ID string
    """
    session_id = payload.get('session_id') or payload.get('sessionId')
    
    if not session_id:
        # Generate new session ID if not provided
        session_id = str(uuid.uuid4())
        logger.info(f"Generated new session ID: {session_id}")
    
    return session_id


def _get_or_create_session(session_id: str, user_id: Optional[str] = None) -> TastingSession:
    """Get existing session or create new one.
    
    Args:
        session_id: Session identifier
        user_id: Optional user identifier
        
    Returns:
        TastingSession object
    """
    session = get_session_state(session_id)
    
    if session is None:
        logger.info(f"Creating new session: {session_id}")
        session = create_new_session(session_id, user_id)
    else:
        logger.info(f"Retrieved existing session: {session_id}")
    
    return session


def _update_session_history(
    session: TastingSession,
    user_message: str,
    assistant_response: str
) -> None:
    """Update session conversation history.
    
    Args:
        session: TastingSession to update
        user_message: User's message
        assistant_response: Agent's response
    """
    # Add user message
    session.conversation_history.append(
        Message(role="user", content=user_message)
    )
    
    # Add assistant response
    session.conversation_history.append(
        Message(role="assistant", content=assistant_response)
    )


def _format_response(
    response: str,
    session_id: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Format agent response for AgentCore.
    
    Args:
        response: Agent's response text
        session_id: Session identifier
        metadata: Optional additional metadata
        
    Returns:
        Formatted response dictionary
    """
    result = {
        "response": response,
        "session_id": session_id,
        "status": "success"
    }
    
    if metadata:
        result["metadata"] = metadata
    
    return result


@app.entrypoint
def agent_invocation(payload: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main entrypoint handler for agent invocations.
    
    This handler:
    1. Extracts user message and session ID from payload
    2. Retrieves or creates session state
    3. Invokes the Beer Tasting Agent
    4. Updates session history
    5. Saves session state
    6. Returns formatted response
    
    Args:
        payload: Request payload containing user message and session info
        context: AgentCore context object
        
    Returns:
        Dictionary with agent response and session information
        
    Raises:
        ValueError: If payload is invalid
        Exception: For unexpected errors during processing
        
    Validates: Requirements 7.1, 7.3 - AgentCore integration and API endpoint
    """
    try:
        logger.info("Agent invocation started")
        logger.debug(f"Payload: {payload}")
        
        # Extract user message
        user_message = _extract_user_message(payload)
        logger.info(f"User message: {user_message[:100]}...")
        
        # Extract or generate session ID
        session_id = _extract_session_id(payload)
        
        # Extract optional user ID
        user_id = payload.get('user_id') or payload.get('userId')
        
        # Get or create session
        session = _get_or_create_session(session_id, user_id)
        
        # Invoke agent with message
        logger.info("Invoking Beer Tasting Agent")
        result = agent(user_message)
        
        # Extract response text
        if hasattr(result, 'content'):
            assistant_response = result.content
        elif isinstance(result, dict):
            assistant_response = result.get('content') or result.get('response') or str(result)
        else:
            assistant_response = str(result)
        
        logger.info(f"Agent response: {assistant_response[:100]}...")
        
        # Update session history
        _update_session_history(session, user_message, assistant_response)
        
        # Save updated session state
        save_session_state(session_id, session)
        logger.info(f"Session state saved: {session_id}")
        
        # Format and return response
        response = _format_response(
            response=assistant_response,
            session_id=session_id,
            metadata={
                "beers_tasted_count": len(session.beers_tasted),
                "has_preference_profile": session.preference_profile is not None,
                "message_count": len(session.conversation_history)
            }
        )
        
        logger.info("Agent invocation completed successfully")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return {
            "response": "Lo siento, hubo un problema con tu mensaje. ¿Podrías intentarlo de nuevo?",
            "session_id": payload.get('session_id', 'unknown'),
            "status": "error",
            "error": str(e)
        }
        
    except Exception as e:
        logger.error(f"Unexpected error during agent invocation: {str(e)}", exc_info=True)
        return {
            "response": "Lo siento, ocurrió un error inesperado. Por favor, intenta de nuevo en un momento.",
            "session_id": payload.get('session_id', 'unknown'),
            "status": "error",
            "error": "Internal server error"
        }


def main():
    """Main entry point for local development and testing."""
    logger.info("Starting Beer Tasting Agent with AgentCore Runtime")
    logger.info(f"AWS Region: {AWS_REGION}")
    logger.info(f"Bedrock Model: {BEDROCK_MODEL_ID}")
    
    # Run the AgentCore application
    app.run()


if __name__ == "__main__":
    main()
