# Bot Installation & Deployment Guide

## 🔧 Requirements

- Python 3.8+
- Git (optional)
- Docker (optional)
- Telegram Bot Token

## 📱 Get Your Telegram Bot Token

1. Open Telegram dan cari [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow the instructions
4. Copy your token

Contoh token: `123456789:ABCdefGHIjklMNOpqrsTUVwxyzABCdef-Gh`

## 🚀 Local Installation (Recommended untuk development)

### Step 1: Clone dan Setup

```bash
# Clone repository
git clone <repo-url>
cd exploi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure

```bash
# Copy template
cp .env.example .env

# Edit .env dengan text editor favorit
# Add your TELEGRAM_TOKEN
```

File `.env` setelah edit:
```env
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyzABCdef-Gh
ADMIN_ID=1234567890
```

### Step 4: Run Bot

```bash
python main.py
```

Kamu sekarang bisa chat dengan bot di Telegram!

## 🐳 Docker Installation

### Quick Start with Docker Compose

```bash
# 1. Clone
git clone <repo-url>
cd exploi

# 2. Setup .env
cp .env.example .env
# Edit .env dengan token

# 3. Run with Docker Compose
docker-compose up -d

# 4. Check logs
docker-compose logs -f scraper-bot

# 5. Stop
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t super-scraper-bot .

# Run container
docker run -d \
  --name scraper-bot \
  -e TELEGRAM_TOKEN=YOUR_TOKEN \
  -e ADMIN_ID=YOUR_ID \
  super-scraper-bot

# Check logs
docker logs -f scraper-bot

# Stop
docker stop scraper-bot
docker rm scraper-bot
```

## ☁️ Cloud Deployment

### Heroku (Free tier sudah discontinued, tapi bisa pakai alternatif)

#### Option 1: Railway

1. Push ke GitHub
2. Connect repo ke [Railway.app](https://railway.app)
3. Set environment variables
4. Deploy

#### Option 2: Replit

1. Create Replit project
2. Upload files
3. Create `.env` file dengan token
4. Run `python main.py`

#### Option 3: VPS (Recommended)

```bash
# SSH ke VPS
ssh your_vps

# Clone repository
git clone <repo-url>
cd exploi

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup .env
nano .env
# Paste token

# Run in background (gunakan screen atau systemd)
screen -S bot
python main.py
# Press Ctrl+A then D to detach

# Or gunakan systemd (lebih professional)
sudo nano /etc/systemd/system/scraper-bot.service
```

Systemd service file:
```ini
[Unit]
Description=Super Scraper Bot
After=network.target

[Service]
Type=simple
User=bot_user
WorkingDirectory=/home/bot_user/exploi
ExecStart=/home/bot_user/exploi/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable scraper-bot
sudo systemctl start scraper-bot
sudo systemctl status scraper-bot
```

## 🧪 Testing

```bash
# Run examples
python examples.py

# Run tests
pip install pytest
python -m pytest test_scrapers.py -v
```

## 📊 Monitoring

### Local
Bot logs tampil di console saat running.

### Docker
```bash
docker-compose logs -f scraper-bot
```

### VPS (Systemd)
```bash
journalctl -u scraper-bot -f
```

### Custom Logging
Edit `config.py`:
```python
LOG_LEVEL = 'DEBUG'  # более verbose logging
```

## 🔒 Security Best Practices

1. **Never commit `.env`**
   - Already in `.gitignore`

2. **Use strong tokens**
   - Regenerate jika bocor

3. **Limit access**
   - Set `ADMIN_ID` untuk admin-only features

4. **Update dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

5. **Monitor logs**
   - Cek error logs secara berkala

## 🛠️ Troubleshooting

### Bot not responding

```bash
# Check if bot is running
ps aux | grep main.py

# Check logs untuk error
python main.py

# Restart
# Ctrl+C untuk stop
# python main.py untuk start ulang
```

### Token invalid

```bash
# Verify token di .env
cat .env | grep TELEGRAM_TOKEN

# Get new token dari @BotFather
# Update .env
# Restart
```

### Memory usage tinggi

```python
# Di config.py, kurangi cache TTL
CACHE_TTL = 1800  # 30 minutes instead of 1 hour

# Atau disable caching
CACHE_ENABLED = False
```

## 📈 Performance Tips

1. **Use specific scrapers** - Lebih cepat daripada generic
2. **Enable caching** - Default sudah enabled
3. **Adjust timeout** - Sesuaikan dengan network
4. **Run on good VPS** - Lebih stabil dari laptop

## 🚀 Next Steps

1. Read [README.md](README.md) untuk overview
2. Read [GUIDE.md](GUIDE.md) untuk detailed documentation
3. Customize `scrapers.py` sesuai kebutuhan
4. Add custom commands di `handlers.py`

---

**Need help?**
- Check error messages carefully
- Read logs dengan teliti
- Test locally dulu sebelum deploy
- Ask di GitHub discussions

Happy scraping! 🎉
