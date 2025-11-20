"""
Application settings and configuration management.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # AWS Configuration
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Bedrock Model Configuration
    BEDROCK_MODEL_ID = os.getenv(
        "BEDROCK_MODEL_ID",
        "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    )
    
    # AgentCore Configuration
    AGENTCORE_ENDPOINT = os.getenv("AGENTCORE_ENDPOINT")
    
    # Cache Configuration
    CACHE_TTL_HOURS = int(os.getenv("CACHE_TTL_HOURS", "24"))
    
    # Scraping Configuration
    BEER_CATALOG_URL = os.getenv(
        "BEER_CATALOG_URL",
        "https://cervezafortuna.com/inicio/cervezas/"
    )
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# Create a singleton instance
settings = Settings()
