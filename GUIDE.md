# 🚀 PANDUAN LENGKAP SUPER SCRAPER BOT

Dokumentasi komprehensif untuk menggunakan dan mengembangkan Super Scraper Bot.

## 📖 Daftar Isi

1. [Installation](#installation)
2. [Konfigurasi](#konfigurasi)
3. [Usage](#usage)
4. [Scripting](#scripting)
5. [Custom Scrapers](#custom-scrapers)
6. [API Reference](#api-reference)
7. [Troubleshooting](#troubleshooting)
8. [Performance](#performance)

## Installation

### Requirements
- Python 3.8+
- pip (Python package manager)
- Internet connection

### Steps

#### 1. Clone Repository
```bash
git clone <repository-url>
cd exploi
```

#### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate:
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate          # Windows
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup Configuration
```bash
cp .env.example .env
# Edit .env and add your TELEGRAM_TOKEN
```

#### Alternative: Auto Setup
```bash
bash setup.sh  # Linux/Mac
```

## Konfigurasi

### File `.env`

```env
# Wajib
TELEGRAM_TOKEN=YOUR_TOKEN_HERE
ADMIN_ID=YOUR_ID_HERE

# Optional - Default values sudah ada
TIMEOUT=10
MAX_RETRIES=3
CACHE_ENABLED=True
CACHE_TTL=3600
LOG_LEVEL=INFO
```

### File `config.py`

Edit untuk customize:
```python
# Waktu timeout (detik)
TIMEOUT = 10

# Berapa kali retry jika gagal
MAX_RETRIES = 3

# User-Agent untuk HTTP requests
USER_AGENT = 'Mozilla/5.0 ...'

# Enable/disable caching
CACHE_ENABLED = True

# Cache lifetime (detik)
CACHE_TTL = 3600  # 1 jam
```

## Usage

### Running the Bot

```bash
python main.py
```

Bot akan mulai berjalan dan siap menerima command.

### Available Commands

#### `/start`
Menampilkan welcome message dan daftar command.
```
/start
```

#### `/help`
Menampilkan bantuan lengkap.
```
/help
```

#### `/news`
Ambil berita terkini dari BBC.
```
/news
```

#### `/quote`
Ambil quote inspiratif harian.
```
/quote
```

#### `/crypto`
Lihat harga cryptocurrency.
```
/crypto
```

#### `/weather [city]`
Cek cuaca untuk kota tertentu.
```
/weather Jakarta
/weather New York
/weather London
```

#### `/scrape [url]`
Scrape konten dari URL.
```
/scrape https://example.com
/scrape https://news.ycombinator.com
```

#### `/table [url]`
Extract tabel dari halaman.
```
/table https://example.com/table
```

#### `/links [url]`
Ambil semua links dari halaman.
```
/links https://example.com
```

## Scripting

### Running Examples

```bash
python examples.py
```

Ini akan menjalankan berbagai contoh penggunaan scrapers.

### Custom Script

Buat file `my_script.py`:

```python
from scrapers import NewsScraper
from utils import DataProcessor

# Ambil berita
scraper = NewsScraper()
news = scraper.get_bbc_news()

# Display
for item in news:
    print(f"- {item['title']}")

# Format message
msg = DataProcessor.format_list(
    [n['title'] for n in news],
    "Latest News"
)
print(msg)
```

Run:
```bash
python my_script.py
```

## Custom Scrapers

### Membuat Scraper Custom

```python
from utils import WebScraper

class MyCustomScraper(WebScraper):
    def scrape_something(self, url):
        # Fetch URL
        html = self.fetch_url(url)
        if not html:
            return None
        
        # Parse
        soup = self.parse_html(html)
        
        # Extract data
        title = self.extract_text(soup.find('h1'))
        link = self.extract_link(soup.find('a'))
        
        return {
            'title': title,
            'link': link
        }

# Usage
scraper = MyCustomScraper()
data = scraper.scrape_something('https://example.com')
print(data)
```

### Menambah Command Baru

1. Edit `handlers.py`:
```python
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """My custom command"""
    msg = await my_scraper.get_data()
    await update.message.reply_text(msg, parse_mode='Markdown')
```

2. Edit `main.py`:
```python
from handlers import my_command

application.add_handler(CommandHandler("mycommand", my_command))
```

3. Use in Telegram:
```
/mycommand
```

## API Reference

### WebScraper Class

```python
from utils import WebScraper

scraper = WebScraper(timeout=10, user_agent='...')

# Fetch URL
html = scraper.fetch_url('https://example.com')

# Parse HTML
soup = scraper.parse_html(html)

# Extract text
text = scraper.extract_text(element)

# Extract link
link = scraper.extract_link(element)
```

### DataProcessor Class

```python
from utils import DataProcessor

# Format message
msg = DataProcessor.format_message(
    'Title',
    {'key': 'value'},
    'Source'
)

# Format list
msg = DataProcessor.format_list(['item1', 'item2'], 'Title')

# Truncate text
short = DataProcessor.truncate_text(long_text, 500)
```

### Cache Class

```python
from utils import cache

# Set
cache.set('mykey', 'myvalue')

# Get
value = cache.get('mykey')

# Clear
cache.clear()
```

### Scrapers

#### NewsScraper
```python
news = scraper.get_bbc_news()
news = scraper.get_generic_news('https://...')
```

#### QuoteScraper
```python
quote = scraper.get_daily_quote()
quotes = scraper.get_quotes_by_author('Steve Jobs')
```

#### CryptoScraper
```python
prices = scraper.get_crypto_prices()
```

#### WeatherScraper
```python
weather = scraper.get_weather('Jakarta')
```

#### GenericScraper
```python
tables = scraper.scrape_table('https://...')
links = scraper.scrape_links('https://...')
content = scraper.scrape_content('https://...', selector='p')
```

## Troubleshooting

### Bot tidak berjalan

**Error: "No module named 'telegram'"**
```bash
pip install -r requirements.txt
```

**Error: "TELEGRAM_TOKEN not valid"**
- Check `.env` file
- Verify token dari @BotFather
- Token harus valid dan lengkap

**Error: Connection timeout**
- Check internet connection
- Naikkan `TIMEOUT` di config.py
- Coba lagi nanti

### Scraper tidak bekerja

**Halaman tidak bisa diakses**
```python
# Check requests
import requests
response = requests.get(url)
print(response.status_code)  # Harus 200
```

**Parser error**
```python
# Debug HTML
html = scraper.fetch_url(url)
print(html[:500])  # Lihat raw HTML
```

**Selector tidak match**
```python
# Find correct selector
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())  # Pretty print untuk debug
```

## Performance

### Optimization Tips

1. **Enable Caching**
```python
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour
```

2. **Adjust Timeout**
```python
TIMEOUT = 15  # Balance antara speed dan reliability
```

3. **Use Specific Selectors**
```python
# Good
content = scraper.scrape_content(url, 'article.main-content')

# Bad (slow)
content = scraper.scrape_content(url)
```

4. **Limit Results**
```python
# Soup select with limit
for item in soup.select('article', limit=10):
    # Process only 10 items
    pass
```

5. **Batch Operations**
```python
# Run multiple scrapers in parallel
import asyncio
from utils import WebScraper

async def batch_scrape():
    scraper = WebScraper()
    tasks = [
        scraper.fetch_url_async(url1),
        scraper.fetch_url_async(url2),
        scraper.fetch_url_async(url3),
    ]
    results = await asyncio.gather(*tasks)
    return results
```

---

**Need more help?** Check README.md or create an issue on GitHub.
