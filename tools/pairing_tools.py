"""
Food pairing tools for the Beer Tasting Agent.

Provides minimal tools for data access. The agent handles all pairing logic.
Validates: Requirements 5.1, 5.2, 5.3
"""
import logging

from strands import tool

logger = logging.getLogger(__name__)


# This file intentionally contains no tools.
# The agent will use its knowledge of beer and food pairing to provide recommendations.
#
# The agent should:
# - Use fetch_beer_catalog_page to get beer data
# - Apply its own knowledge of food pairing principles
# - Generate pairing suggestions based on beer styles and characteristics
# - Explain why pairings work using its understanding of flavor profiles
