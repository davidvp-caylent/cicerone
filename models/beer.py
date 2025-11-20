"""Beer data models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Beer:
    """Represents a beer from the catalog.
    
    Validates: Requirements 1.1 - Beer information must include name, style, ABV, IBU, and description
    """
    id: str
    name: str
    style: str
    abv: float  # Alcohol by Volume
    ibu: Optional[int]  # International Bitterness Units
    description: str
    image_url: Optional[str] = None
    
    def __post_init__(self):
        """Validate beer data after initialization."""
        if not self.id or not isinstance(self.id, str):
            raise ValueError("Beer id must be a non-empty string")
        
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Beer name must be a non-empty string")
        
        if not self.style or not isinstance(self.style, str):
            raise ValueError("Beer style must be a non-empty string")
        
        if not isinstance(self.abv, (int, float)) or self.abv < 0 or self.abv > 20:
            raise ValueError("Beer ABV must be a number between 0 and 20")
        
        if self.ibu is not None:
            if not isinstance(self.ibu, int) or self.ibu < 0 or self.ibu > 120:
                raise ValueError("Beer IBU must be an integer between 0 and 120")
        
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Beer description must be a non-empty string")
        
        if self.image_url is not None and not isinstance(self.image_url, str):
            raise ValueError("Beer image_url must be a string or None")


@dataclass
class BeerDetails:
    """Extended beer information with detailed tasting notes and brewing details."""
    beer: Beer
    tasting_notes: Optional[str] = None
    ingredients: Optional[str] = None
    brewing_process: Optional[str] = None
    food_pairings: Optional[list[str]] = None
    
    def __post_init__(self):
        """Validate beer details after initialization."""
        if not isinstance(self.beer, Beer):
            raise ValueError("BeerDetails must contain a valid Beer object")
        
        if self.tasting_notes is not None and not isinstance(self.tasting_notes, str):
            raise ValueError("Tasting notes must be a string or None")
        
        if self.ingredients is not None and not isinstance(self.ingredients, str):
            raise ValueError("Ingredients must be a string or None")
        
        if self.brewing_process is not None and not isinstance(self.brewing_process, str):
            raise ValueError("Brewing process must be a string or None")
        
        if self.food_pairings is not None:
            if not isinstance(self.food_pairings, list):
                raise ValueError("Food pairings must be a list or None")
            if not all(isinstance(p, str) for p in self.food_pairings):
                raise ValueError("All food pairings must be strings")
