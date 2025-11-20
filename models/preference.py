"""Preference profile data model."""

from dataclasses import dataclass, field


@dataclass
class PreferenceProfile:
    """User's beer preferences based on tasting session feedback.
    
    Validates: Requirements 2.3, 8.1 - Preference recording and storage
    """
    preferred_styles: list[str] = field(default_factory=list)
    bitterness_preference: str = "medium"  # "low", "medium", "high"
    alcohol_tolerance: str = "moderate"  # "light", "moderate", "strong"
    flavor_notes: list[str] = field(default_factory=list)  # ["citrus", "caramel", "coffee", etc.]
    body_preference: str = "medium"  # "light", "medium", "full"
    
    def __post_init__(self):
        """Validate preference profile after initialization."""
        if not isinstance(self.preferred_styles, list):
            raise ValueError("Preferred styles must be a list")
        if not all(isinstance(s, str) for s in self.preferred_styles):
            raise ValueError("All preferred styles must be strings")
        
        valid_bitterness = ["low", "medium", "high"]
        if self.bitterness_preference not in valid_bitterness:
            raise ValueError(f"Bitterness preference must be one of {valid_bitterness}")
        
        valid_alcohol = ["light", "moderate", "strong"]
        if self.alcohol_tolerance not in valid_alcohol:
            raise ValueError(f"Alcohol tolerance must be one of {valid_alcohol}")
        
        if not isinstance(self.flavor_notes, list):
            raise ValueError("Flavor notes must be a list")
        if not all(isinstance(n, str) for n in self.flavor_notes):
            raise ValueError("All flavor notes must be strings")
        
        valid_body = ["light", "medium", "full"]
        if self.body_preference not in valid_body:
            raise ValueError(f"Body preference must be one of {valid_body}")
