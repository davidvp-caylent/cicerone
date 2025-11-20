"""Tasting session data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .preference import PreferenceProfile


@dataclass
class Message:
    """Represents a message in the conversation history."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate message after initialization."""
        valid_roles = ["user", "assistant"]
        if self.role not in valid_roles:
            raise ValueError(f"Message role must be one of {valid_roles}")
        
        if not self.content or not isinstance(self.content, str):
            raise ValueError("Message content must be a non-empty string")
        
        if not isinstance(self.timestamp, datetime):
            raise ValueError("Message timestamp must be a datetime object")


@dataclass
class BeerEvaluation:
    """User's evaluation of a specific beer during tasting.
    
    Validates: Requirements 2.3 - Recording user feedback on beer characteristics
    """
    beer_id: str
    appearance_notes: Optional[str] = None
    aroma_notes: Optional[str] = None
    taste_notes: Optional[str] = None
    mouthfeel_notes: Optional[str] = None
    overall_rating: Optional[int] = None  # 1-5
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate beer evaluation after initialization."""
        if not self.beer_id or not isinstance(self.beer_id, str):
            raise ValueError("Beer ID must be a non-empty string")
        
        if self.appearance_notes is not None and not isinstance(self.appearance_notes, str):
            raise ValueError("Appearance notes must be a string or None")
        
        if self.aroma_notes is not None and not isinstance(self.aroma_notes, str):
            raise ValueError("Aroma notes must be a string or None")
        
        if self.taste_notes is not None and not isinstance(self.taste_notes, str):
            raise ValueError("Taste notes must be a string or None")
        
        if self.mouthfeel_notes is not None and not isinstance(self.mouthfeel_notes, str):
            raise ValueError("Mouthfeel notes must be a string or None")
        
        if self.overall_rating is not None:
            if not isinstance(self.overall_rating, int) or self.overall_rating < 1 or self.overall_rating > 5:
                raise ValueError("Overall rating must be an integer between 1 and 5")
        
        if not isinstance(self.timestamp, datetime):
            raise ValueError("Timestamp must be a datetime object")


@dataclass
class TastingSession:
    """Represents a complete tasting session with user preferences and evaluations.
    
    Validates: Requirements 8.1 - Session state management and preference storage
    """
    session_id: str
    user_id: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.now)
    beers_tasted: list[str] = field(default_factory=list)  # IDs of beers tasted
    evaluations: dict[str, BeerEvaluation] = field(default_factory=dict)
    preference_profile: Optional[PreferenceProfile] = None
    conversation_history: list[Message] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate tasting session after initialization."""
        if not self.session_id or not isinstance(self.session_id, str):
            raise ValueError("Session ID must be a non-empty string")
        
        if self.user_id is not None and not isinstance(self.user_id, str):
            raise ValueError("User ID must be a string or None")
        
        if not isinstance(self.started_at, datetime):
            raise ValueError("Started at must be a datetime object")
        
        if not isinstance(self.beers_tasted, list):
            raise ValueError("Beers tasted must be a list")
        if not all(isinstance(b, str) for b in self.beers_tasted):
            raise ValueError("All beer IDs in beers_tasted must be strings")
        
        if not isinstance(self.evaluations, dict):
            raise ValueError("Evaluations must be a dictionary")
        for beer_id, evaluation in self.evaluations.items():
            if not isinstance(beer_id, str):
                raise ValueError("All evaluation keys must be strings")
            if not isinstance(evaluation, BeerEvaluation):
                raise ValueError("All evaluation values must be BeerEvaluation objects")
        
        if self.preference_profile is not None and not isinstance(self.preference_profile, PreferenceProfile):
            raise ValueError("Preference profile must be a PreferenceProfile object or None")
        
        if not isinstance(self.conversation_history, list):
            raise ValueError("Conversation history must be a list")
        if not all(isinstance(m, Message) for m in self.conversation_history):
            raise ValueError("All conversation history items must be Message objects")
