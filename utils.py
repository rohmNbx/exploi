"""
Utility functions untuk scraping dan processing data
"""
import logging
import asyncio
from typing import Optional, Dict, List
import aiohttp
from bs4 import BeautifulSoup
import requests
from config import USER_AGENT, TIMEOUT, MAX_RETRIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """Main scraper class untuk berbagai tujuan"""
    
    def __init__(self, timeout: int = TIMEOUT, user_agent: str = USER_AGENT):
        self.timeout = timeout
        self.headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    async def fetch_url_async(self, url: str) -> Optional[str]:
        """Fetch URL secara async"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=self.timeout) as response:
                    if response.status == 200:
                        return await response.text()
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
        return None
    
    def fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL secara synchronous dengan retry"""
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < MAX_RETRIES - 1:
                    asyncio.sleep(1)
        return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'html.parser')
    
    def extract_text(self, element) -> str:
        """Extract clean text from element"""
        if element:
            return element.get_text(strip=True)
        return ""
    
    def extract_link(self, element) -> str:
        """Extract link from element"""
        if element and element.get('href'):
            return element['href']
        return ""


class DataProcessor:
    """Olah dan format data untuk ditampilkan"""
    
    @staticmethod
    def format_message(title: str, data: Dict, source: str = "") -> str:
        """Format data menjadi message yang readable"""
        msg = f"*{title}*\n\n"
        
        for key, value in data.items():
            if value:
                msg += f"• *{key}*: {value}\n"
        
        if source:
            msg += f"\n_Sumber: {source}_"
        
        return msg
    
    @staticmethod
    def format_list(items: List[str], title: str = "") -> str:
        """Format list items menjadi message"""
        msg = f"*{title}*\n" if title else ""
        for i, item in enumerate(items, 1):
            msg += f"{i}. {item}\n"
        return msg
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 500) -> str:
        """Potong text jika terlalu panjang"""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text


class Cache:
    """Simple cache system"""
    
    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl
        self.timestamps = {}
    
    def get(self, key: str) -> Optional:
        """Get value from cache"""
        if key in self.cache:
            import time
            if time.time() - self.timestamps[key] < self.ttl:
                logger.info(f"Cache hit: {key}")
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        return None
    
    def set(self, key: str, value) -> None:
        """Set value to cache"""
        import time
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
        self.timestamps.clear()


# Global cache instance
cache = Cache()
