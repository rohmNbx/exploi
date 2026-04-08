"""
Berbagai scraper untuk sumber data berbeda
"""
import logging
from typing import List, Dict, Optional
from utils import WebScraper, cache, CACHE_ENABLED
from config import CACHE_TTL

logger = logging.getLogger(__name__)


class NewsScraper(WebScraper):
    """Scraper untuk berita terkini"""
    
    SOURCES = {
        'bbc': 'https://www.bbc.com/news',
        'reuters': 'https://www.reuters.com',
        'cnn': 'https://www.cnn.com',
    }
    
    def get_bbc_news(self) -> List[Dict]:
        """Scrape BBC News"""
        cache_key = 'bbc_news'
        if CACHE_ENABLED:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        try:
            html = self.fetch_url(self.SOURCES['bbc'])
            if not html:
                return []
            
            soup = self.parse_html(html)
            news = []
            
            # BBC specific selectors
            for article in soup.find_all('h2', limit=5):
                title = self.extract_text(article)
                if title:
                    news.append({
                        'title': title,
                        'source': 'BBC News'
                    })
            
            if CACHE_ENABLED:
                cache.set(cache_key, news, CACHE_TTL)
            
            return news
        except Exception as e:
            logger.error(f"Error scraping BBC: {e}")
            return []
    
    def get_generic_news(self, url: str) -> List[Dict]:
        """Scrape berita dari URL umum"""
        try:
            html = self.fetch_url(url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            news = []
            
            # Coba berbagai selector umum
            selectors = ['h1', 'h2', 'article', '.news', '.article']
            
            for selector in selectors:
                for item in soup.select(selector, limit=5):
                    text = self.extract_text(item)
                    if text and len(text) > 20:
                        news.append({
                            'title': text,
                            'url': url
                        })
                if news:
                    break
            
            return news
        except Exception as e:
            logger.error(f"Error scraping generic news: {e}")
            return []


class QuoteScraper(WebScraper):
    """Scraper untuk quotes inspiratif"""
    
    def get_daily_quote(self) -> Optional[Dict]:
        """Ambil quote harian dari quotable.io"""
        cache_key = 'daily_quote'
        if CACHE_ENABLED:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        try:
            import httpx
            response = httpx.get('https://api.quotable.io/random', timeout=5)
            if response.status_code == 200:
                data = response.json()
                quote = {
                    'text': data.get('content', ''),
                    'author': data.get('author', 'Unknown'),
                    'tags': ', '.join(data.get('tags', []))
                }
                if CACHE_ENABLED:
                    cache.set(cache_key, quote, CACHE_TTL)
                return quote
        except Exception as e:
            logger.error(f"Error fetching quote: {e}")
        
        return None
    
    def get_quotes_by_author(self, author: str) -> List[Dict]:
        """Dapatkan quotes dari author tertentu"""
        try:
            import httpx
            response = httpx.get(
                'https://api.quotable.io/quotes',
                params={'author': author, 'limit': 10},
                timeout=5
            )
            if response.status_code == 200:
                quotes = []
                for item in response.json().get('results', []):
                    quotes.append({
                        'text': item.get('content', ''),
                        'author': item.get('author', ''),
                    })
                return quotes
        except Exception as e:
            logger.error(f"Error fetching quotes: {e}")
        
        return []


class CryptoScraper(WebScraper):
    """Scraper untuk harga cryptocurrency"""
    
    def get_crypto_prices(self) -> Optional[Dict]:
        """Dapatkan harga crypto terkini"""
        cache_key = 'crypto_prices'
        if CACHE_ENABLED:
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        try:
            import httpx
            response = httpx.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={
                    'ids': 'bitcoin,ethereum,cardano',
                    'vs_currencies': 'usd',
                    'include_market_cap': 'true',
                    'include_24hr_vol': 'true'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                prices = response.json()
                if CACHE_ENABLED:
                    cache.set(cache_key, prices, 300)  # Cache 5 menit
                return prices
        except Exception as e:
            logger.error(f"Error fetching crypto prices: {e}")
        
        return None


class WeatherScraper(WebScraper):
    """Scraper untuk informasi cuaca"""
    
    def get_weather(self, city: str) -> Optional[Dict]:
        """Dapatkan cuaca untuk kota tertentu"""
        try:
            import httpx
            # Menggunakan Open-Meteo (free, no API key needed)
            response = httpx.get(
                'https://geocoding-api.open-meteo.com/v1/search',
                params={'name': city, 'count': 1, 'language': 'en', 'format': 'json'},
                timeout=5
            )
            
            if response.status_code != 200 or not response.json().get('results'):
                return None
            
            location = response.json()['results'][0]
            
            # Get weather data
            weather_response = httpx.get(
                'https://api.open-meteo.com/v1/forecast',
                params={
                    'latitude': location['latitude'],
                    'longitude': location['longitude'],
                    'current': 'temperature_2m,weather_code,wind_speed_10m',
                    'timezone': 'auto'
                },
                timeout=5
            )
            
            if weather_response.status_code == 200:
                current = weather_response.json()['current']
                return {
                    'city': city,
                    'temperature': f"{current['temperature_2m']}°C",
                    'wind_speed': f"{current['wind_speed_10m']} km/h",
                    'weather_code': current['weather_code']
                }
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
        
        return None


class GenericScraper(WebScraper):
    """Scraper umum untuk website apapun"""
    
    def scrape_table(self, url: str) -> List[List[str]]:
        """Scrape tabel dari halaman"""
        try:
            html = self.fetch_url(url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            tables = []
            
            for table in soup.find_all('table', limit=1):
                rows = []
                for tr in table.find_all('tr', limit=10):
                    cols = [self.extract_text(td) for td in tr.find_all(['td', 'th'])]
                    if cols:
                        rows.append(cols)
                tables.append(rows)
            
            return tables
        except Exception as e:
            logger.error(f"Error scraping table: {e}")
            return []
    
    def scrape_links(self, url: str) -> List[Dict]:
        """Scrape semua links dari halaman"""
        try:
            html = self.fetch_url(url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            links = []
            
            for a in soup.find_all('a', limit=20):
                link = {
                    'text': self.extract_text(a),
                    'href': self.extract_link(a)
                }
                if link['href'] and link['text']:
                    links.append(link)
            
            return links
        except Exception as e:
            logger.error(f"Error scraping links: {e}")
            return []
    
    def scrape_content(self, url: str, selector: str = "") -> List[str]:
        """Scrape content menggunakan CSS selector"""
        try:
            html = self.fetch_url(url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            contents = []
            
            if selector:
                elements = soup.select(selector, limit=10)
            else:
                elements = soup.find_all(['p', 'div', 'article'], limit=10)
            
            for elem in elements:
                text = self.extract_text(elem)
                if text:
                    contents.append(text)
            
            return contents
        except Exception as e:
            logger.error(f"Error scraping content: {e}")
            return []
