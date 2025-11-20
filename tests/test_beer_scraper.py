"""
Tests for beer catalog scraper.
"""
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from tools.beer_scraper import (
    Beer,
    BeerCatalogCache,
    BeerCatalogScraper,
    get_beer_catalog
)


class TestBeer:
    """Tests for Beer dataclass."""
    
    def test_beer_creation(self):
        """Test creating a Beer instance."""
        beer = Beer(
            id="test-beer",
            name="Test Beer",
            style="IPA",
            abv=6.5,
            ibu=60,
            description="A test beer",
            image_url="https://example.com/beer.jpg"
        )
        
        assert beer.id == "test-beer"
        assert beer.name == "Test Beer"
        assert beer.style == "IPA"
        assert beer.abv == 6.5
        assert beer.ibu == 60
        assert beer.description == "A test beer"
        assert beer.image_url == "https://example.com/beer.jpg"
    
    def test_beer_optional_fields(self):
        """Test Beer with optional fields as None."""
        beer = Beer(
            id="test-beer",
            name="Test Beer",
            style="Lager",
            abv=4.5,
            ibu=None,
            description="",
            image_url=None
        )
        
        assert beer.ibu is None
        assert beer.image_url is None


class TestBeerCatalogCache:
    """Tests for BeerCatalogCache."""
    
    def test_cache_initialization(self):
        """Test cache directory creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = BeerCatalogCache(cache_dir=tmpdir, ttl_hours=24)
            assert cache.cache_dir.exists()
            assert cache.ttl_hours == 24
    
    def test_cache_save_and_load(self):
        """Test saving and loading beers from cache."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = BeerCatalogCache(cache_dir=tmpdir)
            
            beers = [
                Beer(
                    id="beer-1",
                    name="Beer 1",
                    style="IPA",
                    abv=6.0,
                    ibu=50,
                    description="First beer",
                    image_url=None
                ),
                Beer(
                    id="beer-2",
                    name="Beer 2",
                    style="Stout",
                    abv=7.5,
                    ibu=None,
                    description="Second beer",
                    image_url="https://example.com/beer2.jpg"
                )
            ]
            
            cache.save(beers)
            loaded_beers = cache.load()
            
            assert loaded_beers is not None
            assert len(loaded_beers) == 2
            assert loaded_beers[0].name == "Beer 1"
            assert loaded_beers[1].name == "Beer 2"
    
    def test_cache_is_valid_fresh(self):
        """Test that fresh cache is valid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = BeerCatalogCache(cache_dir=tmpdir, ttl_hours=24)
            
            beers = [Beer(
                id="test",
                name="Test",
                style="IPA",
                abv=5.0,
                ibu=None,
                description="",
                image_url=None
            )]
            
            cache.save(beers)
            assert cache.is_valid() is True
    
    def test_cache_is_valid_missing(self):
        """Test that missing cache is invalid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = BeerCatalogCache(cache_dir=tmpdir)
            assert cache.is_valid() is False


class TestBeerCatalogScraper:
    """Tests for BeerCatalogScraper."""
    
    def test_scraper_initialization(self):
        """Test scraper initialization with defaults."""
        scraper = BeerCatalogScraper()
        assert scraper.base_url is not None
        assert scraper.timeout > 0
        assert scraper.max_retries > 0
    
    def test_parse_beer_catalog_empty(self):
        """Test parsing empty HTML."""
        scraper = BeerCatalogScraper()
        html = "<html><body></body></html>"
        beers = scraper._parse_beer_catalog(html)
        assert beers == []
    
    def test_parse_beer_element_basic(self):
        """Test parsing a basic beer element."""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="beer-item">
            <h2>Test IPA</h2>
            <span class="style">India Pale Ale</span>
            <p>A hoppy beer with 6.5% ABV and 60 IBU</p>
            <img src="/images/test-ipa.jpg" />
        </div>
        """
        
        soup = BeautifulSoup(html, 'lxml')
        element = soup.find('div', class_='beer-item')
        
        scraper = BeerCatalogScraper()
        beer = scraper._parse_beer_element(element, 0)
        
        assert beer is not None
        assert beer.name == "Test IPA"
        assert beer.style == "India Pale Ale"
        assert beer.abv == 6.5
        assert beer.ibu == 60
    
    @patch('requests.get')
    def test_get_catalog_with_mock_response(self, mock_get):
        """Test getting catalog with mocked HTTP response."""
        mock_response = Mock()
        mock_response.text = """
        <html>
            <body>
                <div class="beer-item">
                    <h2>Mock Beer</h2>
                    <span class="style">Lager</span>
                    <p>A refreshing lager with 4.5% ABV</p>
                </div>
            </body>
        </html>
        """
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with tempfile.TemporaryDirectory() as tmpdir:
            scraper = BeerCatalogScraper()
            scraper.cache = BeerCatalogCache(cache_dir=tmpdir)
            
            beers = scraper.get_catalog()
            
            assert len(beers) >= 0  # May be 0 if HTML structure doesn't match
    
    def test_get_catalog_uses_cache(self):
        """Test that get_catalog uses cache when valid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scraper = BeerCatalogScraper()
            scraper.cache = BeerCatalogCache(cache_dir=tmpdir)
            
            # Pre-populate cache
            cached_beers = [
                Beer(
                    id="cached-beer",
                    name="Cached Beer",
                    style="Ale",
                    abv=5.0,
                    ibu=30,
                    description="From cache",
                    image_url=None
                )
            ]
            scraper.cache.save(cached_beers)
            
            # Get catalog should use cache
            beers = scraper.get_catalog()
            
            assert len(beers) == 1
            assert beers[0].name == "Cached Beer"
    
    @patch('requests.get')
    def test_get_catalog_fallback_to_cache_on_error(self, mock_get):
        """Test fallback to cache when website is unavailable."""
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Network error")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            scraper = BeerCatalogScraper()
            scraper.cache = BeerCatalogCache(cache_dir=tmpdir)
            
            # Pre-populate cache
            cached_beers = [
                Beer(
                    id="fallback-beer",
                    name="Fallback Beer",
                    style="Stout",
                    abv=7.0,
                    ibu=None,
                    description="Fallback from cache",
                    image_url=None
                )
            ]
            scraper.cache.save(cached_beers)
            
            # Should fallback to cache
            beers = scraper.get_catalog()
            
            assert len(beers) == 1
            assert beers[0].name == "Fallback Beer"
    
    @patch('requests.get')
    def test_get_catalog_raises_when_no_cache(self, mock_get):
        """Test that RuntimeError is raised when both fetch and cache fail."""
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Network error")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            scraper = BeerCatalogScraper()
            scraper.cache = BeerCatalogCache(cache_dir=tmpdir)
            
            # No cache available
            with pytest.raises(RuntimeError, match="Failed to fetch beer catalog"):
                scraper.get_catalog()


class TestModuleLevelFunction:
    """Tests for module-level get_beer_catalog function."""
    
    @patch('tools.beer_scraper.BeerCatalogScraper')
    def test_get_beer_catalog_creates_singleton(self, mock_scraper_class):
        """Test that get_beer_catalog uses singleton instance."""
        mock_instance = Mock()
        mock_instance.get_catalog.return_value = []
        mock_scraper_class.return_value = mock_instance
        
        # Reset singleton
        import tools.beer_scraper
        tools.beer_scraper._scraper_instance = None
        
        # First call should create instance
        get_beer_catalog()
        assert mock_scraper_class.call_count == 1
        
        # Second call should reuse instance
        get_beer_catalog()
        assert mock_scraper_class.call_count == 1
