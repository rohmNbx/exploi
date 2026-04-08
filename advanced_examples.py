"""
Contoh-contoh advanced usage untuk Super Scraper Bot
"""

from scrapers import NewsScraper, QuoteScraper, CryptoScraper, WeatherScraper, GenericScraper
from advanced_scrapers import AdvancedScraper, FeedScraper
from utils import DataProcessor, cache
import asyncio


# ============================================================================
# EXAMPLE 1: Extract Metadata dari Halaman
# ============================================================================

def example_metadata():
    """Extract SEO metadata, OpenGraph, dll"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Extract Metadata")
    print("="*60 + "\n")
    
    scraper = AdvancedScraper()
    url = "https://www.python.org"
    
    metadata = scraper.scrape_metadata(url)
    print(f"Metadata dari {url}:\n")
    
    for key, value in list(metadata.items())[:10]:
        print(f"{key}: {value}")


# ============================================================================
# EXAMPLE 2: Parse JSON-LD Structured Data
# ============================================================================

def example_json_ld():
    """Extract structured data JSON-LD"""
    print("\n" + "="*60)
    print("EXAMPLE 2: JSON-LD Structured Data")
    print("="*60 + "\n")
    
    scraper = AdvancedScraper()
    url = "https://www.example.com"
    
    json_ld = scraper.scrape_json_ld(url)
    
    if json_ld:
        print(f"Found {len(json_ld)} JSON-LD objects:\n")
        for i, data in enumerate(json_ld, 1):
            print(f"{i}. Type: {data.get('@type', 'Unknown')}")
            print(f"   Data: {str(data)[:100]}...\n")
    else:
        print("No JSON-LD data found")


# ============================================================================
# EXAMPLE 3: Extract Images dari Halaman
# ============================================================================

def example_images():
    """Extract semua images"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Extract Images")
    print("="*60 + "\n")
    
    scraper = AdvancedScraper()
    url = "https://www.example.com"
    
    images = scraper.scrape_images(url)
    
    if images:
        print(f"Found {len(images)} images:\n")
        for i, img in enumerate(images[:5], 1):
            print(f"{i}. Image: {img['src'][:50]}...")
            if img['alt']:
                print(f"   Alt: {img['alt']}")
    else:
        print("No images found")


# ============================================================================
# EXAMPLE 4: Extract Headings untuk SEO Analysis
# ============================================================================

def example_headings():
    """Extract heading structure untuk SEO"""
    print("\n" + "="*60)
    print("EXAMPLE 4: SEO Headings Analysis")
    print("="*60 + "\n")
    
    scraper = AdvancedScraper()
    url = "https://www.python.org"
    
    headings = scraper.scrape_headings(url)
    
    print(f"Heading structure dari {url}:\n")
    for level, heading_list in headings.items():
        if heading_list:
            print(f"{level.upper()}: ({len(heading_list)} items)")
            for heading in heading_list[:3]:
                truncated = DataProcessor.truncate_text(heading, 60)
                print(f"  - {truncated}")
    
    # SEO Analysis
    h1_count = len(headings.get('h1', []))
    print(f"\n📊 SEO Notes:")
    print(f"  H1 count: {h1_count} (ideal: 1)")
    if h1_count != 1:
        print(f"  ⚠️  Page has {h1_count} H1 tags (should be exactly 1)")


# ============================================================================
# EXAMPLE 5: Extract Forms dari Halaman
# ============================================================================

def example_forms():
    """Extract form information"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Extract Forms")
    print("="*60 + "\n")
    
    scraper = AdvancedScraper()
    url = "https://www.example.com"
    
    forms = scraper.scrape_forms(url)
    
    if forms:
        print(f"Found {len(forms)} forms:\n")
        for i, form in enumerate(forms, 1):
            print(f"{i}. Form")
            print(f"   Action: {form['action']}")
            print(f"   Method: {form['method']}")
            print(f"   Fields: {len(form['fields'])}")
            
            for field in form['fields'][:3]:
                print(f"     - {field['name']} ({field['type']})")
    else:
        print("No forms found")


# ============================================================================
# EXAMPLE 6: Parse RSS Feed
# ============================================================================

def example_rss_feed():
    """Parse RSS feed untuk news"""
    print("\n" + "="*60)
    print("EXAMPLE 6: RSS Feed Parser")
    print("="*60 + "\n")
    
    scraper = FeedScraper()
    
    feeds = {
        'HN': 'https://news.ycombinator.com/rss',
        'TechCrunch': 'https://techcrunch.com/feed/',
    }
    
    for feed_name, feed_url in feeds.items():
        print(f"\n📰 {feed_name} Feed:\n")
        entries = scraper.parse_feed(feed_url)
        
        for i, entry in enumerate(entries[:3], 1):
            title = DataProcessor.truncate_text(entry['title'], 60)
            print(f"{i}. {title}")
            if entry.get('published'):
                print(f"   📅 {entry['published'][:10]}")
            print()


# ============================================================================
# EXAMPLE 7: Scrape dengan Custom Selector
# ============================================================================

def example_custom_selector():
    """Scrape dengan CSS selector custom"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Custom CSS Selector")
    print("="*60 + "\n")
    
    scraper = GenericScraper()
    url = "https://www.example.com"
    
    # Contoh: scrape paragraf dengan class tertentu
    contents = scraper.scrape_content(url, selector='p.intro')
    
    print(f"Content with 'p.intro' selector:\n")
    for i, content in enumerate(contents[:3], 1):
        truncated = DataProcessor.truncate_text(content, 100)
        print(f"{i}. {truncated}\n")
    
    # Bisa customize selector sesuai kebutuhan:
    # 'article.post' - artikle dengan class post
    # 'div[data-id]' - div dengan attribute data-id
    # '.container > .item' - item dalam container
    # '#main p' - paragraf dalam element dengan id main


# ============================================================================
# EXAMPLE 8: Batch Scraping Multiple Sources
# ============================================================================

def example_batch_scrape():
    """Scrape multiple sources sekaligus"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Batch Scraping")
    print("="*60 + "\n")
    
    urls_to_scrape = [
        "https://www.example.com",
        "https://example.org",
        "https://test.example.net"
    ]
    
    scraper = GenericScraper()
    print(f"Scraping {len(urls_to_scrape)} URLs...\n")
    
    results = {}
    for url in urls_to_scrape:
        print(f"⏳ Scraping {url}...")
        content = scraper.scrape_content(url)
        results[url] = len(content)
        print(f"✓ Found {len(content)} content items\n")
    
    # Summary
    print("SUMMARY:")
    for url, count in results.items():
        print(f"  {url}: {count} items")


# ============================================================================
# EXAMPLE 9: Caching Demonstration
# ============================================================================

def example_caching():
    """Demonstrate caching untuk performance"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Caching System")
    print("="*60 + "\n")
    
    print("First call (tanpa cache):")
    scraper = QuoteScraper()
    quote1 = scraper.get_daily_quote()
    print(f"Got quote: {quote1['text'][:50]}...\n")
    
    print("Second call (dari cache):")
    quote2 = scraper.get_daily_quote()
    print(f"Got quote: {quote2['text'][:50]}...")
    print("(This is dari cache, jauh lebih cepat!)\n")
    
    # Clear cache
    print("Clearing cache...")
    cache.clear()
    print("✓ Cache cleared\n")


# ============================================================================
# EXAMPLE 10: Data Processing & Formatting
# ============================================================================

def example_formatting():
    """Format data untuk display optimal"""
    print("\n" + "="*60)
    print("EXAMPLE 10: Data Processing & Formatting")
    print("="*60 + "\n")
    
    # Format message dari dict
    weather = {
        'Temperature': '25°C',
        'Humidity': '60%',
        'Wind': '10 km/h',
        'Condition': 'Partly Cloudy'
    }
    
    msg = DataProcessor.format_message('Jakarta Weather', weather, 'OpenWeatherMap')
    print("Formatted Message:\n")
    print(msg)
    
    # Format list
    print("\n" + "-"*40 + "\n")
    items = ['Python', 'JavaScript', 'Go', 'Rust', 'TypeScript']
    list_msg = DataProcessor.format_list(items, 'Top Programming Languages 2024')
    print("Formatted List:\n")
    print(list_msg)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run semua examples"""
    examples = [
        ("Metadata", example_metadata),
        ("JSON-LD", example_json_ld),
        ("Images", example_images),
        ("Headings", example_headings),
        ("Forms", example_forms),
        ("RSS Feed", example_rss_feed),
        ("Custom Selector", example_custom_selector),
        ("Batch Scraping", example_batch_scrape),
        ("Caching", example_caching),
        ("Formatting", example_formatting),
    ]
    
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "🤖 SUPER SCRAPER BOT - ADVANCED EXAMPLES".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    print(f"\nAvailable examples: {len(examples)}\n")
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"{i:2d}. {name}")
    
    while True:
        try:
            choice = input("\nEnter example number (1-10) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(examples):
                _, func = examples[choice_num - 1]
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("Invalid choice!")
        
        except (ValueError, KeyboardInterrupt):
            break
    
    print("\n\n👋 Thanks for using Super Scraper Bot!\n")


if __name__ == '__main__':
    main()
