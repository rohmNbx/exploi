"""
Contoh penggunaan Script untuk Super Scraper Bot
Jalankan contoh berbeda untuk test berbagai fitur
"""

from scrapers import (
    NewsScraper, QuoteScraper, CryptoScraper,
    WeatherScraper, GenericScraper
)
from utils import DataProcessor


def example_news():
    """Contoh: Scraping berita"""
    print("\n📰 EXAMPLE: SCRAPING BERITA\n")
    
    scraper = NewsScraper()
    news = scraper.get_bbc_news()
    
    if news:
        for i, item in enumerate(news, 1):
            print(f"{i}. {item['title']}")
            print(f"   Source: {item['source']}\n")
    else:
        print("Tidak ada berita ditemukan")


def example_quotes():
    """Contoh: Ambil quote"""
    print("\n✨ EXAMPLE: QUOTE INSPIRATIF\n")
    
    scraper = QuoteScraper()
    quote = scraper.get_daily_quote()
    
    if quote:
        print(f'"{quote["text"]}"')
        print(f"— {quote['author']}")
        print(f"Tags: {quote['tags']}")
    else:
        print("Tidak bisa mengambil quote")


def example_crypto():
    """Contoh: Harga cryptocurrency"""
    print("\n💰 EXAMPLE: CRYPTOCURRENCY PRICES\n")
    
    scraper = CryptoScraper()
    prices = scraper.get_crypto_prices()
    
    if prices:
        for crypto, data in prices.items():
            if isinstance(data, dict) and 'usd' in data:
                print(f"{crypto.upper()}: ${data['usd']:,}")
    else:
        print("Tidak bisa mengambil harga crypto")


def example_weather():
    """Contoh: Data cuaca"""
    print("\n🌤️ EXAMPLE: WEATHER\n")
    
    scraper = WeatherScraper()
    
    cities = ['Jakarta', 'Surabaya', 'Bandung']
    for city in cities:
        weather = scraper.get_weather(city)
        if weather:
            print(f"{city}:")
            print(f"  Temperature: {weather['temperature']}")
            print(f"  Wind Speed: {weather['wind_speed']}\n")


def example_scrape_content():
    """Contoh: Scrape konten dari website"""
    print("\n📄 EXAMPLE: SCRAPE CONTENT\n")
    
    scraper = GenericScraper()
    url = "https://www.python.org"
    
    print(f"Scraping {url}...\n")
    contents = scraper.scrape_content(url)
    
    for i, content in enumerate(contents[:3], 1):
        truncated = DataProcessor.truncate_text(content, 100)
        print(f"{i}. {truncated}\n")


def example_scrape_links():
    """Contoh: Ambil semua links"""
    print("\n🔗 EXAMPLE: SCRAPE LINKS\n")
    
    scraper = GenericScraper()
    url = "https://www.python.org"
    
    print(f"Scraping links dari {url}...\n")
    links = scraper.scrape_links(url)
    
    for i, link in enumerate(links[:5], 1):
        print(f"{i}. {link['text']}")
        print(f"   URL: {link['href']}\n")


def example_data_formatting():
    """Contoh: Format data untuk display"""
    print("\n🎨 EXAMPLE: DATA FORMATTING\n")
    
    # Format message
    data = {
        'Temperature': '25°C',
        'Humidity': '60%',
        'Wind Speed': '10 km/h'
    }
    msg = DataProcessor.format_message('Weather Report', data, 'OpenWeatherMap')
    print(msg)
    
    # Format list
    print("\n")
    items = ['Python', 'JavaScript', 'Go', 'Rust']
    list_msg = DataProcessor.format_list(items, 'Top Programming Languages')
    print(list_msg)


def main():
    """Run semua contoh"""
    print("=" * 60)
    print("🤖 SUPER SCRAPER BOT - EXAMPLES")
    print("=" * 60)
    
    try:
        example_news()
        example_quotes()
        example_crypto()
        example_weather()
        example_scrape_content()
        example_scrape_links()
        example_data_formatting()
        
        print("\n" + "=" * 60)
        print("✅ Semua contoh berhasil dijalankan!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
