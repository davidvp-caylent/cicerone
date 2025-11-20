"""
Recommendation tools for the Beer Tasting Agent.

Provides minimal tools for data access. The agent handles all recommendation logic.
Validates: Requirements 3.2, 3.3, 2.4
"""
import logging

from strands import tool

logger = logging.getLogger(__name__)


# This file intentionally contains no tools.
# The agent will use the catalog and preference tools to build recommendations
# using its own reasoning and logic.
#
# The agent should:
# - Use fetch_beer_catalog_page to get beer data
# - Use get_evaluations to see what the user has tasted
# - Use get_preferences to understand user preferences
# - Apply its own logic to predict favorites and suggest tasting order
