# Super Scraper Bot 🤖

Bot Telegram ultimate untuk scraping informasi dari sumber apapun dengan kemampuan yang powerful dan fleksibel!

## ✨ Fitur Utama

- 📰 **Scraping Berita** - Ambil berita terkini dari berbagai sumber
- 📊 **Harga Crypto** - Real-time cryptocurrency prices (Bitcoin, Ethereum, etc)
- 🌤️ **Data Cuaca** - Informasi cuaca untuk kota manapun
- ✨ **Quote Harian** - Quote motivasi & inspiratif
- 🌐 **Generic Scraper** - Scrape website apapun dengan CSS selector
- 📊 **Table Extractor** - Extract tabel dari halaman
- 🔗 **Link Scraper** - Ambil semua link dari halaman
- ⚡ **Smart Caching** - Caching otomatis untuk performa lebih baik
- 🔄 **Retry Logic** - Retry otomatis jika koneksi gagal

## 🚀 Quick Start

### 1. Setup Environment

Clone repository:
```bash
git clone <repo_url>
cd exploi
```

Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Bot

Copy `.env.example` ke `.env` dan isi dengan token bot Telegram Anda:

```bash
cp .env.example .env
```

Buka `.env` dan masukkan:
```
TELEGRAM_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_ID=YOUR_TELEGRAM_ID_HERE
```

**Cara mendapat token:**
1. Chat dengan [@BotFather](https://t.me/botfather) di Telegram
2. Kirim `/newbot` untuk membuat bot baru
3. Ikuti instruksi dan dapatkan token Anda

### 4. Run Bot

```bash
python main.py
```

Bot sekarang siap menerima command dari Telegram!

## 📋 Command Reference

| Command | Deskripsi | Contoh |
|---------|-----------|---------|
| `/start` | Mulai bot | `/start` |
| `/help` | Lihat semua command | `/help` |
| `/news` | Berita terkini | `/news` |
| `/quote` | Quote harian | `/quote` |
| `/crypto` | Harga cryptocurrency | `/crypto` |
| `/weather` | Cuaca di kota | `/weather Jakarta` |
| `/scrape` | Scrape URL | `/scrape https://example.com` |
| `/table` | Extract tabel | `/table https://example.com/data` |
| `/links` | Ambil semua link | `/links https://example.com` |

## 🛠️ Project Structure

```
exploi/
├── main.py              # Entry point bot
├── config.py            # Konfigurasi utama
├── handlers.py          # Handler untuk setiap command
├── scrapers.py          # Berbagai scraper implementation
├── utils.py             # Utility functions & helpers
├── requirements.txt     # Dependencies
├── .env.example         # Template konfigurasi
├── .env                 # Konfigurasi aktual (local only)
├── .gitignore          # Git ignore rules
└── README.md           # File ini
```

## 📚 Dokumentasi Fitur

### NewsScraper
Scrape berita dari BBC News dan website berita lainnya:
```python
from scrapers import NewsScraper
scraper = NewsScraper()
news = scraper.get_bbc_news()
```

### QuoteScraper
Ambil quote dari API quotable.io:
```python
from scrapers import QuoteScraper
scraper = QuoteScraper()
quote = scraper.get_daily_quote()
```

### CryptoScraper
Get harga crypto dari CoinGecko:
```python
from scrapers import CryptoScraper
scraper = CryptoScraper()
prices = scraper.get_crypto_prices()
```

### WeatherScraper
Get cuaca menggunakan Open-Meteo API (Free):
```python
from scrapers import WeatherScraper
scraper = WeatherScraper()
weather = scraper.get_weather('Jakarta')
```

### GenericScraper
Scrape custom website dengan flexible options:
```python
from scrapers import GenericScraper
scraper = GenericScraper()

# Scrape content
content = scraper.scrape_content('https://example.com')

# Extract links
links = scraper.scrape_links('https://example.com')

# Extract tables
tables = scraper.scrape_table('https://example.com/data')
```

## ⚙️ Konfigurasi

Semua setting dapat di-customize di file `config.py`:

```python
# Timeout untuk requests (detik)
TIMEOUT = 10

# Jumlah retry jika gagal
MAX_RETRIES = 3

# Enable/disable caching
CACHE_ENABLED = True

# Cache TTL (detik)
CACHE_TTL = 3600  # 1 jam

# Log level
LOG_LEVEL = 'INFO'
```

## 🔐 Security & Privacy

- ✅ Bot hanya menyimpan data minimal
- ✅ Tidak ada data sensitif yang disimpan
- ✅ Menggunakan HTTPS untuk semua request
- ✅ User data tidak di-share dengan pihak ketiga
- ✅ Caching lokal hanya di memory

## 🐛 Troubleshooting

### Bot tidak merespon?
1. Pastikan token di `.env` benar
2. Cek internet connection
3. Lihat log: `python main.py` akan menampilkan error

### Error "No module named..."?
```bash
pip install -r requirements.txt
```

### Timeout error?
Naikkan `TIMEOUT` di `config.py`:
```python
TIMEOUT = 20  # 20 detik
```

### Cache issue?
Clear cache dengan:
```python
from utils import cache
cache.clear()
```

## 📦 Dependencies

- **python-telegram-bot** - Telegram Bot API wrapper
- **requests** - HTTP library
- **beautifulsoup4** - HTML parsing
- **httpx** - Modern HTTP client
- **selenium** - Browser automation (optional)
- **python-dotenv** - Environment variables
- **lxml** - XML/HTML processing

## 🚀 Advanced Usage

### Custom Scraper

Buat scraper custom dengan extend base class:

```python
from utils import WebScraper, DataProcessor

class MyCustomScraper(WebScraper):
    def get_data(self, url):
        html = self.fetch_url(url)
        soup = self.parse_html(html)
        
        # Custom parsing logic here
        data = {
            'title': self.extract_text(soup.find('h1')),
            'description': self.extract_text(soup.find('p'))
        }
        
        return data
```

### Add Custom Command

Edit `handlers.py` dan `main.py`:

```python
# Di handlers.py
async def my_custom_command(update, context):
    await update.message.reply_text("Response aku!")

# Di main.py
application.add_handler(CommandHandler("mycmd", my_custom_command))
```

## 📈 Performance Tips

1. **Enable Caching** - Reduce API calls significantly
2. **Adjust Timeout** - Balance antara speed dan reliability
3. **Use Selectors** - CSS selectors lebih efisien dari parsing penuh
4. **Batch Requests** - Combine multiple operations

## 🤝 Contributing

Contributions welcome! Silakan:
1. Fork repository
2. Create feature branch
3. Make your changes
4. Submit pull request

## 📝 License

MIT License - feel free to use for personal/commercial projects

## 📞 Support

Punya pertanyaan? Issues? Suggestions?

Buat issue di GitHub atau contact maintainer

---

**Happy Scraping!** 🎉

Dibuat dengan ❤️ untuk community

