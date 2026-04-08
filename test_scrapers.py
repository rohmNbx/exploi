"""
Unit tests untuk Super Scraper Bot
Jalankan dengan: python -m pytest test_scrapers.py -v
"""

import pytest
from scrapers import NewsScraper, QuoteScraper, CryptoScraper, WeatherScraper, GenericScraper
from utils import DataProcessor, Cache, WebScraper


class TestWebScraper:
    """Test WebScraper base class"""
    
    def test_scraper_init(self):
        scraper = WebScraper()
        assert scraper.timeout > 0
        assert 'User-Agent' in scraper.headers
    
    def test_extract_text(self):
        from bs4 import BeautifulSoup
        html = '<p>Test Text</p>'
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('p')
        
        scraper = WebScraper()
        result = scraper.extract_text(element)
        assert result == 'Test Text'


class TestDataProcessor:
    """Test data processing utilities"""
    
    def test_truncate_text(self):
        text = "a" * 600
        result = DataProcessor.truncate_text(text, 500)
        assert len(result) <= 503  # 500 + "..."
        assert result.endswith("...")
    
    def test_format_message(self):
        data = {"Key1": "Value1", "Key2": "Value2"}
        result = DataProcessor.format_message("Title", data)
        assert "Title" in result
        assert "Key1" in result
        assert "Value1" in result
    
    def test_format_list(self):
        items = ["Item1", "Item2", "Item3"]
        result = DataProcessor.format_list(items, "Test List")
        assert "Test List" in result
        assert "1. Item1" in result
        assert "2. Item2" in result


class TestCache:
    """Test caching system"""
    
    def test_cache_set_get(self):
        cache = Cache(ttl=3600)
        cache.set("key1", "value1")
        result = cache.get("key1")
        assert result == "value1"
    
    def test_cache_miss(self):
        cache = Cache()
        result = cache.get("nonexistent")
        assert result is None
    
    def test_cache_clear(self):
        cache = Cache()
        cache.set("key1", "value1")
        cache.clear()
        result = cache.get("key1")
        assert result is None


class TestQuoteScraper:
    """Test quote scraper"""
    
    def test_quote_structure(self):
        scraper = QuoteScraper()
        quote = scraper.get_daily_quote()
        
        if quote:  # API mungkin down, so if it works:
            assert 'text' in quote
            assert 'author' in quote
            assert len(quote['text']) > 0


class TestCryptoScraper:
    """Test crypto scraper"""
    
    def test_crypto_structure(self):
        scraper = CryptoScraper()
        prices = scraper.get_crypto_prices()
        
        if prices:
            for crypto, data in prices.items():
                assert isinstance(data, dict)


class TestWeatherScraper:
    """Test weather scraper"""
    
    def test_weather_not_found(self):
        scraper = WeatherScraper()
        weather = scraper.get_weather("XYZ_NONEXISTENT_CITY_12345")
        assert weather is None
    
    def test_weather_valid_city(self):
        scraper = WeatherScraper()
        weather = scraper.get_weather("Jakarta")
        
        if weather:
            assert 'temperature' in weather
            assert 'wind_speed' in weather


class TestGenericScraper:
    """Test generic scraper"""
    
    def test_scraper_empty_url(self):
        scraper = GenericScraper()
        result = scraper.scrape_links("")
        assert result == [] or isinstance(result, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
