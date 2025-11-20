"""
Preference tools for the Beer Tasting Agent.

Provides tools for storing and retrieving user preference data.
The agent will handle the analysis logic.
Validates: Requirements 3.1, 3.2, 8.1, 8.4
"""
import logging
from typing import Dict, Any

from strands import tool

logger = logging.getLogger(__name__)


@tool
def store_preference(session_id: str, preference_key: str, preference_value: Any) -> dict:
    """
    Store a user preference for the current session.
    
    Saves a preference key-value pair associated with a session ID.
    The agent can use this to remember user preferences during the tasting session.
    
    Validates: Requirements 8.1 - Store preferences in profile
    
    Args:
        session_id: The unique session identifier
        preference_key: The preference key (e.g., "bitterness_preference", "favorite_styles")
        preference_value: The preference value (can be string, number, list, etc.)
        
    Returns:
        Dictionary containing:
            - success: Boolean indicating if storage succeeded
            - session_id: The session ID
            - key: The preference key stored
    """
    import json
    from pathlib import Path
    
    try:
        # Create sessions directory
        sessions_dir = Path(".cache/sessions")
        sessions_dir.mkdir(parents=True, exist_ok=True)
        
        session_file = sessions_dir / f"{session_id}.json"
        
        # Load existing session data or create new
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
        else:
            session_data = {"preferences": {}, "evaluations": []}
        
        # Store preference
        session_data["preferences"][preference_key] = preference_value
        
        # Save back to file
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Stored preference '{preference_key}' for session {session_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "key": preference_key
        }
    
    except Exception as e:
        logger.error(f"Failed to store preference: {e}")
        return {
            "success": False,
            "error": "Storage failed",
            "message": str(e)
        }


@tool
def get_preferences(session_id: str) -> dict:
    """
    Retrieve all stored preferences for a session.
    
    Gets all preference data associated with a session ID.
    
    Validates: Requirements 8.1 - Retrieve stored preferences
    
    Args:
        session_id: The unique session identifier
        
    Returns:
        Dictionary containing:
            - success: Boolean indicating if retrieval succeeded
            - preferences: Dictionary of all stored preferences
            - session_id: The session ID
    """
    import json
    from pathlib import Path
    
    try:
        session_file = Path(f".cache/sessions/{session_id}.json")
        
        if not session_file.exists():
            logger.info(f"No preferences found for session {session_id}")
            return {
                "success": True,
                "preferences": {},
                "session_id": session_id,
                "message": "No preferences stored yet"
            }
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        preferences = session_data.get("preferences", {})
        
        logger.info(f"Retrieved {len(preferences)} preferences for session {session_id}")
        
        return {
            "success": True,
            "preferences": preferences,
            "session_id": session_id
        }
    
    except Exception as e:
        logger.error(f"Failed to get preferences: {e}")
        return {
            "success": False,
            "error": "Retrieval failed",
            "message": str(e)
        }


@tool
def store_evaluation(session_id: str, beer_id: str, evaluation_data: dict) -> dict:
    """
    Store a beer evaluation for the current session.
    
    Saves the user's evaluation of a specific beer, including their notes
    and ratings for appearance, aroma, taste, and mouthfeel.
    
    Validates: Requirements 2.3 - Record user feedback
    
    Args:
        session_id: The unique session identifier
        beer_id: The ID of the beer being evaluated
        evaluation_data: Dictionary containing evaluation details:
            - appearance_notes: Optional appearance feedback
            - aroma_notes: Optional aroma feedback
            - taste_notes: Optional taste feedback
            - mouthfeel_notes: Optional mouthfeel feedback
            - overall_rating: Optional rating (1-5)
            
    Returns:
        Dictionary containing:
            - success: Boolean indicating if storage succeeded
            - session_id: The session ID
            - beer_id: The beer ID
    """
    import json
    from pathlib import Path
    from datetime import datetime
    
    try:
        sessions_dir = Path(".cache/sessions")
        sessions_dir.mkdir(parents=True, exist_ok=True)
        
        session_file = sessions_dir / f"{session_id}.json"
        
        # Load existing session data or create new
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
        else:
            session_data = {"preferences": {}, "evaluations": []}
        
        # Add evaluation with timestamp
        evaluation = {
            "beer_id": beer_id,
            "timestamp": datetime.now().isoformat(),
            **evaluation_data
        }
        
        session_data["evaluations"].append(evaluation)
        
        # Save back to file
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Stored evaluation for beer '{beer_id}' in session {session_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "beer_id": beer_id,
            "total_evaluations": len(session_data["evaluations"])
        }
    
    except Exception as e:
        logger.error(f"Failed to store evaluation: {e}")
        return {
            "success": False,
            "error": "Storage failed",
            "message": str(e)
        }


@tool
def get_evaluations(session_id: str) -> dict:
    """
    Retrieve all beer evaluations for a session.
    
    Gets all evaluation data for beers tasted in this session.
    
    Validates: Requirements 2.3 - Retrieve recorded feedback
    
    Args:
        session_id: The unique session identifier
        
    Returns:
        Dictionary containing:
            - success: Boolean indicating if retrieval succeeded
            - evaluations: List of all beer evaluations
            - session_id: The session ID
    """
    import json
    from pathlib import Path
    
    try:
        session_file = Path(f".cache/sessions/{session_id}.json")
        
        if not session_file.exists():
            logger.info(f"No evaluations found for session {session_id}")
            return {
                "success": True,
                "evaluations": [],
                "session_id": session_id,
                "message": "No evaluations stored yet"
            }
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        evaluations = session_data.get("evaluations", [])
        
        logger.info(f"Retrieved {len(evaluations)} evaluations for session {session_id}")
        
        return {
            "success": True,
            "evaluations": evaluations,
            "session_id": session_id,
            "count": len(evaluations)
        }
    
    except Exception as e:
        logger.error(f"Failed to get evaluations: {e}")
        return {
            "success": False,
            "error": "Retrieval failed",
            "message": str(e)
        }



@tool
def analyze_preferences(session_id: str) -> dict:
    """
    Analyze user preferences from their beer evaluations and construct a preference profile.
    
    This tool retrieves all evaluations for the session and provides them to you
    so you can analyze patterns and construct a PreferenceProfile.
    
    Your task as the agent:
    1. Review all the beer evaluations (notes, ratings) from this session
    2. Identify patterns in what the user likes/dislikes:
       - Which beer styles do they prefer?
       - Do they prefer high, medium, or low bitterness?
       - Do they prefer light, moderate, or strong alcohol content?
       - What flavor notes do they mention positively?
       - Do they prefer light, medium, or full body?
    3. Use store_preference() to save the constructed profile components:
       - preferred_styles: list of beer styles they liked
       - bitterness_preference: "low", "medium", or "high"
       - alcohol_tolerance: "light", "moderate", or "strong"
       - flavor_notes: list of flavor descriptors they enjoyed
       - body_preference: "light", "medium", or "full"
    
    Guidelines for analysis:
    - Look for beers with ratings >= 4 as indicators of preferences
    - Pay attention to positive language in their notes
    - Consider the characteristics (ABV, IBU, style) of highly-rated beers
    - Identify recurring themes across multiple evaluations
    - Be consistent: don't mark contradictory preferences
    
    Validates: Requirements 3.1, 3.2, 8.4
    
    Args:
        session_id: The unique session identifier
        
    Returns:
        Dictionary containing:
            - success: Boolean indicating if analysis can proceed
            - evaluations: List of all beer evaluations with their data
            - evaluation_count: Number of evaluations available
            - message: Instructions or status message
    """
    import json
    from pathlib import Path
    
    try:
        session_file = Path(f".cache/sessions/{session_id}.json")
        
        if not session_file.exists():
            return {
                "success": False,
                "message": "No session data found. User needs to evaluate beers first.",
                "evaluation_count": 0
            }
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        evaluations = session_data.get("evaluations", [])
        
        if len(evaluations) < 2:
            return {
                "success": False,
                "message": f"Only {len(evaluations)} evaluation(s) available. Need at least 2 to analyze patterns.",
                "evaluation_count": len(evaluations)
            }
        
        logger.info(f"Providing {len(evaluations)} evaluations for preference analysis")
        
        return {
            "success": True,
            "evaluations": evaluations,
            "evaluation_count": len(evaluations),
            "message": f"Found {len(evaluations)} evaluations. Analyze the patterns and use store_preference() to save each component of the preference profile."
        }
    
    except Exception as e:
        logger.error(f"Failed to analyze preferences: {e}")
        return {
            "success": False,
            "error": "Analysis failed",
            "message": str(e)
        }
