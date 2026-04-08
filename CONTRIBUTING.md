# Contributing to Super Scraper Bot

Terima kasih sudah tertarik untuk berkontribusi! 🎉

## Code of Conduct

Silakan baca [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) untuk memahami nilai-nilai komunitas kami.

## Cara Berkontribusi

### 1. Report Bug

Jika menemukan bug:
- **Cek** apakah sudah ada issue yang sama
- **Create** issue baru dengan label `bug`
- **Jelaskan** cara reproduce bug
- **Sertakan** error message dan environment

Contoh:
```
Title: Bot crashes when scraping example.com

Environment:
- Python 3.9
- Ubuntu 20.04
- Bot version 1.0.0

Steps to reproduce:
1. Run bot
2. Send /scrape https://example.com
3. Bot crashes

Expected: Bot returns scraped content
Actual: Bot crashes with error...

Error message:
[paste error here]
```

### 2. Suggest Enhancement

Punya ide feature baru?
- **Create** issue dengan label `enhancement`
- **Jelaskan** use case dan benefit
- **Sertakan** contoh kode jika ada

### 3. Submit Pull Request

#### Setup

```bash
# Fork repository
git clone https://github.com/YOUR_USERNAME/exploi.git
cd exploi

# Create branch
git checkout -b feature/your-feature-name

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8
```

#### Development

```bash
# Code sambil mengikuti style guide (PEP 8)
# Use black untuk format
black .

# Check linting
flake8 .

# Run tests
python -m pytest test_scrapers.py -v
```

#### Commit

```bash
# Commit dengan pesan yang jelas
git commit -m "Add: Description of changes"

# Supported prefixes:
# - Add: Fitur baru
# - Fix: Bug fix
# - Improve: Enhancement eksisting
# - Docs: Documentation
# - Test: Test additions
```

#### Push & PR

```bash
# Push ke fork
git push origin feature/your-feature-name

# Create pull request di GitHub
# Jelaskan changes di PR description
```

## Communication

- **Issues**: Untuk bugs dan feature requests
- **Discussions**: Untuk pertanyaan umum
- **Pull Requests**: Untuk kontribusi code

## Code Style

### Python Style

```python
# Good ✓
def get_data(url: str) -> Optional[Dict]:
    """Get data dari URL"""
    if not url:
        return None
    
    result = scraper.fetch(url)
    return result

# Bad ✗
def getData(url):
    if url==None:
        return None
    result=scraper.fetch(url)
    return result
```

### Naming Convention

- `snake_case` untuk functions dan variables
- `CamelCase` untuk classes
- `UPPERCASE` untuk constants

### Documentation

```python
def scrape_news(url: str, limit: int = 10) -> List[Dict]:
    """
    Scrape berita dari URL.
    
    Args:
        url (str): Target URL untuk scraping
        limit (int): Maximum items to return (default: 10)
    
    Returns:
        List[Dict]: List of news items dengan keys:
            - title (str): News title
            - link (str): News link
            - date (str): Publication date
    
    Raises:
        ValueError: Jika URL invalid
        ConnectionError: Jika tidak bisa connect
    
    Example:
        >>> news = scrape_news('https://example.com')
        >>> print(news[0]['title'])
    """
    pass
```

## Directory Structure

```
exploi/
├── main.py              # Bot entry point
├── config.py            # Configuration
├── handlers.py          # Command handlers
├── scrapers.py          # Basic scrapers
├── advanced_scrapers.py # Advanced scrapers
├── utils.py             # Utilities
├── test_scrapers.py     # Tests
├── examples.py          # Basic examples
├── advanced_examples.py # Advanced examples
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

## Testing

```bash
# Run all tests
python -m pytest test_scrapers.py -v

# Run specific test
python -m pytest test_scrapers.py::TestNewsScraper -v

# With coverage
pip install pytest-cov
python -m pytest test_scrapers.py --cov=. --cov-report=html
```

## Documentation

- Update README.md jika ada perubahan major
- Add comments untuk kode yang kompleks
- Update GUIDE.md untuk fitur baru
- Add example di examples.py

## Performance

- ⚡ Gunakan caching untuk API calls
- 🔄 Gunakan async untuk I/O operations
- 📊 Monitor memory usage
- ⏱️ Test dengan various URLs

## Security

- ❌ Jangan commit `.env` files
- 🔒 Validate user input
- 🚫 Jangan expose secret keys
- 📝 Review error messages (jangan leak info)

## Checklist Sebelum Submit PR

- [ ] Code follows style guide
- [ ] Tests pass locally
- [ ] No linting errors (flake8)
- [ ] Code formatted dengan black
- [ ] Added/updated tests jika diperlukan
- [ ] Added/updated documentation
- [ ] No breaking changes (atau jelaskan)
- [ ] Commit messages jelas dan deskriptif

## Help Needed

Kami particularly mencari bantuan di:

- 🐛 Bug fixes
- 🧪 Test coverage
- 📚 Documentation
- 🌍 Translations
- 🎨 UI/UX improvements
- 📊 New scrapers

## Questions?

- Read [README.md](README.md)
- Check [GUIDE.md](GUIDE.md)
- Create discussion
- Email maintainer

---

**Thank you for contributing!** 🙏

Let's make Super Scraper Bot better together! 🚀
