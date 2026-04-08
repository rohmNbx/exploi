#!/bin/bash
# Quick Setup Script untuk Super Scraper Bot
# Run: bash setup.sh

echo "================================"
echo "🤖 Super Scraper Bot - Setup"
echo "================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
python -m venv venv
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate  # For Linux/Mac
# For Windows use: venv\Scripts\activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo ""

# Copy .env template
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your TELEGRAM_TOKEN"
else
    echo "✓ .env file already exists"
fi
echo ""

echo "================================"
echo "✅ Setup complete!"
echo "================================"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env and add your Telegram bot token"
echo "2. Run: python main.py"
echo ""
echo "📚 For more info, read README.md"
echo ""
