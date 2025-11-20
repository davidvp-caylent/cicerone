"""
Beer Catalog Scraper for Cerveza Fortuna website.

This module handles scraping beer information from cervezafortuna.com,
including caching with TTL and error handling with fallback to cached data.
"""
import json
import logging
import os
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class Beer:
    """Represents a beer from the catalog."""
    id: str
    name: str
    style: str
    abv: float  # Alcohol by Volume
    ibu: Optional[int]  # International Bitterness Units
    description: str
    image_url: Optional[str]


class BeerCatalogCache:
    """Manages local cache for beer catalog with TTL."""
    
    def __init__(self, cache_dir: str = ".cache", ttl_hours: int = None):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time-to-live in hours (defaults to settings)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "beer_catalog.json"
        self.ttl_hours = ttl_hours or settings.CACHE_TTL_HOURS
    
    def is_valid(self) -> bool:
        """Check if cache exists and is still valid (within TTL)."""
        if not self.cache_file.exists():
            return False
        
        # Check file modification time
        mtime = datetime.fromtimestamp(self.cache_file.stat().st_mtime)
        age = datetime.now() - mtime
        
        is_valid = age < timedelta(hours=self.ttl_hours)
        if is_valid:
            logger.info(f"Cache is valid (age: {age})")
        else:
            logger.info(f"Cache expired (age: {age}, TTL: {self.ttl_hours}h)")
        
        return is_valid
    
    def load(self) -> Optional[List[Beer]]:
        """Load beer catalog from cache."""
        if not self.cache_file.exists():
            logger.warning("Cache file does not exist")
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            beers = [Beer(**beer_data) for beer_data in data]
            logger.info(f"Loaded {len(beers)} beers from cache")
            return beers
        
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            logger.error(f"Failed to load cache: {e}")
            return None
    
    def save(self, beers: List[Beer]) -> None:
        """Save beer catalog to cache."""
        try:
            data = [asdict(beer) for beer in beers]
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(beers)} beers to cache")
        
        except (IOError, TypeError) as e:
            logger.error(f"Failed to save cache: {e}")


class BeerCatalogScraper:
    """Scrapes beer catalog from Cerveza Fortuna website."""
    
    def __init__(
        self,
        base_url: str = None,
        timeout: int = None,
        max_retries: int = None
    ):
        """
        Initialize scraper.
        
        Args:
            base_url: Base URL for the beer catalog
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url or settings.BEER_CATALOG_URL
        self.timeout = timeout or settings.REQUEST_TIMEOUT
        self.max_retries = max_retries or settings.MAX_RETRIES
        self.cache = BeerCatalogCache()
    
    def _make_request(self, url: str) -> Optional[str]:
        """
        Make HTTP request with retry logic.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if request fails
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{self.max_retries})")
                
                response = requests.get(
                    url,
                    timeout=self.timeout,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (compatible; BeerTastingAgent/1.0)'
                    }
                )
                response.raise_for_status()
                
                logger.info(f"Successfully fetched {url}")
                return response.text
            
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
        
        return None
    
    def _parse_beer_catalog(self, html: str) -> List[Beer]:
        """
        Parse HTML to extract beer information.
        
        Args:
            html: HTML content from the beer catalog page
            
        Returns:
            List of Beer objects
        """
        soup = BeautifulSoup(html, 'lxml')
        beers = []
        
        # Find all beer entries
        # Note: This is a placeholder implementation that needs to be adjusted
        # based on the actual HTML structure of cervezafortuna.com
        beer_elements = soup.find_all('div', class_='beer-item')
        
        if not beer_elements:
            # Try alternative selectors
            beer_elements = soup.find_all('article', class_='product')
        
        if not beer_elements:
            logger.warning("No beer elements found with known selectors")
            # Return empty list rather than failing
            return beers
        
        for idx, element in enumerate(beer_elements):
            try:
                beer = self._parse_beer_element(element, idx)
                if beer:
                    beers.append(beer)
            except Exception as e:
                logger.warning(f"Failed to parse beer element {idx}: {e}")
                continue
        
        logger.info(f"Parsed {len(beers)} beers from HTML")
        return beers
    
    def _parse_beer_element(self, element, idx: int) -> Optional[Beer]:
        """
        Parse a single beer element from HTML.
        
        Args:
            element: BeautifulSoup element containing beer data
            idx: Index for generating beer ID
            
        Returns:
            Beer object or None if parsing fails
        """
        # Extract beer name
        name_elem = element.find(['h2', 'h3', 'h4'], class_=['title', 'product-title', 'beer-name'])
        if not name_elem:
            name_elem = element.find(['h2', 'h3', 'h4'])
        
        if not name_elem:
            logger.warning(f"No name found for beer element {idx}")
            return None
        
        name = name_elem.get_text(strip=True)
        
        # Extract style
        style_elem = element.find(class_=['style', 'beer-style', 'category'])
        style = style_elem.get_text(strip=True) if style_elem else "Unknown"
        
        # Extract ABV
        abv = 0.0
        abv_elem = element.find(string=lambda text: text and 'ABV' in text.upper())
        if abv_elem:
            try:
                # Extract number from text like "5.5% ABV" or "ABV: 5.5%"
                import re
                abv_match = re.search(r'(\d+\.?\d*)\s*%', abv_elem)
                if abv_match:
                    abv = float(abv_match.group(1))
            except (ValueError, AttributeError):
                pass
        
        # Extract IBU
        ibu = None
        ibu_elem = element.find(string=lambda text: text and 'IBU' in text.upper())
        if ibu_elem:
            try:
                import re
                # Look for number followed by or preceded by IBU
                ibu_match = re.search(r'(\d+)\s*IBU|IBU\s*:?\s*(\d+)', ibu_elem, re.IGNORECASE)
                if ibu_match:
                    ibu = int(ibu_match.group(1) or ibu_match.group(2))
            except (ValueError, AttributeError):
                pass
        
        # Extract description
        desc_elem = element.find(['p', 'div'], class_=['description', 'excerpt', 'beer-description'])
        if not desc_elem:
            desc_elem = element.find('p')
        description = desc_elem.get_text(strip=True) if desc_elem else ""
        
        # Extract image URL
        img_elem = element.find('img')
        image_url = None
        if img_elem:
            image_url = img_elem.get('src') or img_elem.get('data-src')
            if image_url and not image_url.startswith('http'):
                image_url = urljoin(self.base_url, image_url)
        
        # Generate ID from name
        beer_id = name.lower().replace(' ', '-').replace('/', '-')
        
        return Beer(
            id=beer_id,
            name=name,
            style=style,
            abv=abv,
            ibu=ibu,
            description=description,
            image_url=image_url
        )
    
    def get_catalog(self, force_refresh: bool = False) -> List[Beer]:
        """
        Get beer catalog, using cache if valid or fetching from website.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of Beer objects
            
        Raises:
            RuntimeError: If both fetching and cache fallback fail
        """
        # Try to use cache if valid and not forcing refresh
        if not force_refresh and self.cache.is_valid():
            cached_beers = self.cache.load()
            if cached_beers:
                logger.info("Using cached beer catalog")
                return cached_beers
        
        # Fetch fresh data from website
        logger.info("Fetching fresh beer catalog from website")
        html = self._make_request(self.base_url)
        
        if html:
            try:
                beers = self._parse_beer_catalog(html)
                
                # Validate that we got some beers
                if beers:
                    self.cache.save(beers)
                    return beers
                else:
                    logger.warning("Parsed 0 beers from website")
            
            except Exception as e:
                logger.error(f"Failed to parse beer catalog: {e}")
        
        # Fallback to cache if website fetch failed
        logger.warning("Website fetch failed, attempting to use cached data")
        cached_beers = self.cache.load()
        
        if cached_beers:
            logger.info(f"Using stale cache as fallback ({len(cached_beers)} beers)")
            return cached_beers
        
        # Both fresh fetch and cache failed
        error_msg = "Failed to fetch beer catalog and no cache available"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


# Module-level function for easy access
_scraper_instance = None


def get_beer_catalog(force_refresh: bool = False) -> List[Beer]:
    """
    Get beer catalog from Cerveza Fortuna.
    
    This is the main entry point for getting the beer catalog.
    Uses caching with 24-hour TTL and falls back to cache on errors.
    
    Args:
        force_refresh: If True, bypass cache and fetch fresh data
        
    Returns:
        List of Beer objects
        
    Raises:
        RuntimeError: If both fetching and cache fallback fail
    """
    global _scraper_instance
    
    if _scraper_instance is None:
        _scraper_instance = BeerCatalogScraper()
    
    return _scraper_instance.get_catalog(force_refresh=force_refresh)
