"""
Catalog tools for the Beer Tasting Agent.

Provides tools for making HTTP requests to retrieve beer catalog data.
The agent will handle parsing and analysis of the data.
Validates: Requirements 1.1, 1.3
"""
import logging
import requests
from urllib.parse import urlparse, urljoin

from strands import tool

logger = logging.getLogger(__name__)

# Allowed domain for beer catalog
ALLOWED_DOMAIN = "cervezafortuna.com"


def _is_url_allowed(url: str) -> tuple[bool, str]:
    """
    Check if a URL is allowed for fetching.
    
    Args:
        url: The URL to check
        
    Returns:
        Tuple of (is_allowed, error_message)
    """
    try:
        parsed = urlparse(url)
        
        # Check domain - only validate domain, allow any path
        if parsed.netloc and parsed.netloc != ALLOWED_DOMAIN:
            return False, f"Domain '{parsed.netloc}' is not allowed. Only '{ALLOWED_DOMAIN}' is permitted."
        
        return True, ""
    
    except Exception as e:
        return False, f"Invalid URL: {str(e)}"


@tool
def fetch_page(url: str) -> dict:
    """
    Fetch HTML content from any page on cervezafortuna.com.
    
    Makes an HTTP GET request to retrieve raw HTML content. The agent can use this
    to explore the entire website, follow links to discover beer information, and
    extract detailed data from any page.
    
    IMPORTANT: Only URLs within cervezafortuna.com domain are allowed.
    The agent can explore any path on the site to discover information.
    
    Validates: Requirements 1.1, 1.3 - Retrieve beer catalog and detail data
    
    Args:
        url: The URL to fetch. Must be within cervezafortuna.com domain.
             Can be a full URL or a relative path (e.g., "/inicio/cervezas/")
        
    Returns:
        Dictionary containing:
            - success: Boolean indicating if request succeeded
            - html: The raw HTML content (if successful)
            - status_code: HTTP status code
            - url: The final URL fetched (after any redirects)
            - error: Error message (if failed)
            
    Examples:
        # Fetch main catalog
        fetch_page("https://cervezafortuna.com/inicio/cervezas/")
        
        # Fetch specific beer page (relative path)
        fetch_page("/inicio/cervezas/ipa-fortuna/")
        
        # Fetch any page on the site
        fetch_page("https://cervezafortuna.com/contacto/")
    """
    try:
        # Handle relative URLs
        if url.startswith("/"):
            url = f"https://{ALLOWED_DOMAIN}{url}"
        
        # Validate URL is allowed
        is_allowed, error_msg = _is_url_allowed(url)
        if not is_allowed:
            logger.warning(f"URL not allowed: {url} - {error_msg}")
            return {
                "success": False,
                "error": "URL not allowed",
                "message": error_msg,
                "allowed_domain": ALLOWED_DOMAIN
            }
        
        logger.info(f"Fetching page from {url}")
        
        response = requests.get(
            url,
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; BeerTastingAgent/1.0)'
            },
            allow_redirects=True
        )
        response.raise_for_status()
        
        logger.info(f"Successfully fetched page (status: {response.status_code})")
        
        return {
            "success": True,
            "html": response.text,
            "status_code": response.status_code,
            "url": response.url,
            "content_length": len(response.text)
        }
    
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout for {url}")
        return {
            "success": False,
            "error": "Request timeout",
            "message": f"The request to {url} timed out after 10 seconds"
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return {
            "success": False,
            "error": "Request failed",
            "message": str(e),
            "url": url
        }


@tool
def get_cached_catalog() -> dict:
    """
    Retrieve the cached beer catalog data if available.
    
    Checks for a locally cached version of the beer catalog and returns it
    if found. This is useful as a fallback when the website is unavailable.
    
    Returns:
        Dictionary containing:
            - success: Boolean indicating if cache was found
            - data: The cached catalog data (if available)
            - cache_age_hours: Age of the cache in hours (if available)
            - error: Error message (if cache not found)
    """
    import json
    from pathlib import Path
    from datetime import datetime
    
    try:
        cache_file = Path(".cache/beer_catalog.json")
        
        if not cache_file.exists():
            logger.info("No cache file found")
            return {
                "success": False,
                "error": "Cache not found",
                "message": "No cached catalog data available"
            }
        
        # Read cache
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Calculate cache age
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        age_hours = (datetime.now() - mtime).total_seconds() / 3600
        
        logger.info(f"Retrieved cache with {len(data)} beers (age: {age_hours:.1f}h)")
        
        return {
            "success": True,
            "data": data,
            "cache_age_hours": round(age_hours, 1),
            "cached_at": mtime.isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to read cache: {e}")
        return {
            "success": False,
            "error": "Cache read failed",
            "message": str(e)
        }


@tool
def save_catalog_cache(catalog_data: list) -> dict:
    """
    Save beer catalog data to local cache.
    
    Stores the provided catalog data in a local JSON file for future use
    as a fallback when the website is unavailable.
    
    Args:
        catalog_data: List of beer dictionaries to cache
        
    Returns:
        Dictionary containing:
            - success: Boolean indicating if save succeeded
            - beers_cached: Number of beers saved
            - error: Error message (if failed)
    """
    import json
    from pathlib import Path
    
    try:
        cache_dir = Path(".cache")
        cache_dir.mkdir(exist_ok=True)
        cache_file = cache_dir / "beer_catalog.json"
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(catalog_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(catalog_data)} beers to cache")
        
        return {
            "success": True,
            "beers_cached": len(catalog_data),
            "cache_file": str(cache_file)
        }
    
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")
        return {
            "success": False,
            "error": "Cache save failed",
            "message": str(e)
        }
