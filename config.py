"""
Konfigurasi Bot Telegram Scraper
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# Bot Settings
BOT_NAME = "Super Scraper Bot 🤖"
BOT_VERSION = "1.0.0"

# Scraping Settings
TIMEOUT = int(os.getenv('TIMEOUT', '10'))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Cache Settings
CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True') == 'True'
CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))  # 1 hour

# Database Settings (Optional)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_data.db')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Supported Scrapers
SUPPORTED_SCRAPERS = {
    'news': 'Scraper untuk berita dari berbagai sumber',
    'weather': 'Informasi cuaca real-time',
    'quotes': 'Quote inspiratif harian',
    'crypto': 'Harga cryptocurrency',
    'stocks': 'Data saham real-time',
    'generic': 'Scraping website umum',
}
