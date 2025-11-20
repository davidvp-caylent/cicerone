"""
Tools module for Beer Tasting Agent.

This module contains minimal tools that provide the agent with capabilities to:
- Fetch web pages from the beer catalog
- Store and retrieve user preferences and evaluations
- Cache data locally

The agent uses these tools along with its own reasoning to:
- Parse HTML and extract beer information
- Analyze user preferences
- Generate recommendations
- Provide food pairings
"""

from tools.catalog_tools import fetch_page, get_cached_catalog, save_catalog_cache
from tools.preference_tools import (
    store_preference,
    get_preferences,
    store_evaluation,
    get_evaluations
)

__all__ = [
    # Catalog tools
    "fetch_page",
    "get_cached_catalog",
    "save_catalog_cache",
    # Preference tools
    "store_preference",
    "get_preferences",
    "store_evaluation",
    "get_evaluations",
]
