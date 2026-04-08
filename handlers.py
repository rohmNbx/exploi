"""
Handler untuk commands Telegram bot
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils import DataProcessor
from scrapers import (
    NewsScraper, QuoteScraper, CryptoScraper, 
    WeatherScraper, GenericScraper
)

logger = logging.getLogger(__name__)

# Initialize scrapers
news_scraper = NewsScraper()
quote_scraper = QuoteScraper()
crypto_scraper = CryptoScraper()
weather_scraper = WeatherScraper()
generic_scraper = GenericScraper()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /start command"""
    user = update.effective_user
    welcome_msg = f"""
Halo {user.first_name}! 👋

Selamat datang di *Super Scraper Bot* 🤖

Aku bisa membantu kamu scrape informasi dari berbagai sumber!

*Perintah Tersedia:*
• /news - Dapatkan berita terkini
• /quote - Quote inspiratif harian
• /crypto - Harga cryptocurrency
• /weather [kota] - Cuaca di kota tertentu
• /scrape [url] - Scrape URL tertentu
• /help - Bantuan lengkap

*Contoh penggunaan:*
`/weather jakarta`
`/scrape https://example.com`

Gunakan menu di bawah atau ketik command dengan `/`
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /help command"""
    help_msg = """
*📖 BANTUAN BOT SCRAPER*

*Perintah Dasar:*

1. `/news` - Dapatkan berita terkini
   Scrape berita dari BBC News otomatis

2. `/quote` - Quote inspiratif harian
   Ambil quote motivasi random setiap hari

3. `/crypto` - Harga cryptocurrency real-time
   Bitcoin, Ethereum, Cardano & lebih banyak

4. `/weather [kota]` - Cuaca untuk kota tertentu
   Contoh: `/weather Jakarta`

5. `/scrape [url]` - Scrape konten dari URL
   Contoh: `/scrape https://example.com`

6. `/table [url]` - Extract tabel dari website
   Contoh: `/table https://example.com/data`

7. `/links [url]` - Ambil semua link dari halaman
   Contoh: `/links https://example.com`

*Fitur Lanjutan:*
• Caching otomatis untuk performa lebih baik
• Support berbagai format data
• Retry otomatis jika koneksi gagal

*Tips:*
- Gunakan URL yang valid
- Tunggu beberapa detik saat pertama kali
- Bot aman & privacy aman

Butuh bantuan lebih? Hubungi admin atau baca dokumentasi.
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')


async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /news command"""
    await update.message.reply_text("⏳ Mengambil berita terkini...", parse_mode='Markdown')
    
    try:
        news = news_scraper.get_bbc_news()
        
        if news:
            msg = "*📰 Berita Terkini dari BBC*\n\n"
            for i, item in enumerate(news[:5], 1):
                title = DataProcessor.truncate_text(item.get('title', ''), 100)
                msg += f"{i}. {title}\n\n"
            
            msg += "_Sumber: BBC News_"
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Tidak bisa mengambil berita saat ini. Coba lagi nanti.",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in get_news: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}",
            parse_mode='Markdown'
        )


async def get_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /quote command"""
    await update.message.reply_text("✨ Mengambil quote inspiratif...", parse_mode='Markdown')
    
    try:
        quote = quote_scraper.get_daily_quote()
        
        if quote:
            msg = f"""*✨ Quote Harian*

"{quote['text']}"

— {quote['author']}

_Tags: {quote.get('tags', 'N/A')}_
"""
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Tidak bisa mengambil quote saat ini.",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in get_quote: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}",
            parse_mode='Markdown'
        )


async def get_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /crypto command"""
    await update.message.reply_text("⏳ Mengambil harga crypto...", parse_mode='Markdown')
    
    try:
        prices = crypto_scraper.get_crypto_prices()
        
        if prices:
            msg = "*💰 Harga Cryptocurrency Terkini*\n\n"
            
            for crypto, data in prices.items():
                if isinstance(data, dict) and 'usd' in data:
                    usd = data['usd']
                    market_cap = data.get('usd_market_cap', 'N/A')
                    msg += f"*{crypto.upper()}*\n"
                    msg += f"  💵 ${usd:,}\n"
                    msg += f"  📊 Market Cap: ${market_cap:,}\n\n"
            
            msg += "_Sumber: CoinGecko API_"
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Tidak bisa mengambil data crypto saat ini.",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in get_crypto: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}",
            parse_mode='Markdown'
        )


async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /weather command"""
    if not context.args:
        await update.message.reply_text(
            "❌ Gunakan: `/weather [nama kota]`\nContoh: `/weather Jakarta`",
            parse_mode='Markdown'
        )
        return
    
    city = ' '.join(context.args)
    await update.message.reply_text(f"⏳ Mengambil data cuaca untuk {city}...", parse_mode='Markdown')
    
    try:
        weather = weather_scraper.get_weather(city)
        
        if weather:
            msg = f"""*🌤️ Cuaca di {weather['city']}*

🌡️ Suhu: {weather['temperature']}
💨 Angin: {weather['wind_speed']}

_Update terkini_
"""
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                f"❌ Kota '{city}' tidak ditemukan.",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in get_weather: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}",
            parse_mode='Markdown'
        )


async def scrape_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /scrape command"""
    if not context.args:
        await update.message.reply_text(
            "❌ Gunakan: `/scrape [url]`\nContoh: `/scrape https://example.com`",
            parse_mode='Markdown'
        )
        return
    
    url = context.args[0]
    await update.message.reply_text(f"⏳ Scraping {url}...", parse_mode='Markdown')
    
    try:
        contents = generic_scraper.scrape_content(url)
        
        if contents:
            msg = f"*📄 Konten dari {url[:50]}...*\n\n"
            for i, content in enumerate(contents[:5], 1):
                truncated = DataProcessor.truncate_text(content, 150)
                msg += f"{i}. {truncated}\n\n"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Tidak bisa mengambil konten dari URL ini.",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in scrape_url: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}",
            parse_mode='Markdown'
        )


async def scrape_table(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /table command"""
    if not context.args:
        await update.message.reply_text(
            "❌ Gunakan: `/table [url]`",
            parse_mode='Markdown'
        )
        return
    
    url = context.args[0]
    await update.message.reply_text(f"⏳ Mengekstrak tabel dari {url}...", parse_mode='Markdown')
    
    try:
        tables = generic_scraper.scrape_table(url)
        
        if tables:
            msg = f"*📊 Tabel dari {url[:50]}...*\n\n"
            for row in tables[0][:10]:
                msg += " | ".join(str(col)[:20] for col in row) + "\n"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Tidak ada tabel ditemukan di halaman ini.",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in scrape_table: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}",
            parse_mode='Markdown'
        )


async def scrape_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk /links command"""
    if not context.args:
        await update.message.reply_text(
            "❌ Gunakan: `/links [url]`",
            parse_mode='Markdown'
        )
        return
    
    url = context.args[0]
    await update.message.reply_text(f"⏳ Mengambil links dari {url}...", parse_mode='Markdown')
    
    try:
        links = generic_scraper.scrape_links(url)
        
        if links:
            msg = f"*🔗 Links dari {url[:50]}...*\n\n"
            for i, link in enumerate(links[:10], 1):
                text = DataProcessor.truncate_text(link['text'], 40)
                href = DataProcessor.truncate_text(link['href'], 50)
                msg += f"{i}. [{text}]({href})\n"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                "❌ Tidak ada link ditemukan di halaman ini.",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in scrape_links: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}",
            parse_mode='Markdown'
        )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler untuk command yang tidak dikenal"""
    await update.message.reply_text(
        "❌ Command tidak dikenal. Ketik `/help` untuk melihat daftar command.",
        parse_mode='Markdown'
    )
