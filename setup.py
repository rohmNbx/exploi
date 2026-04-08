"""
Setup configuration untuk Super Scraper Bot
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="super-scraper-bot",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Bot Telegram super scraping informasi dari berbagai sumber",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/exploi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-telegram-bot==21.1",
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "selenium==4.15.2",
        "lxml==4.9.3",
        "aiohttp==3.9.1",
        "python-dotenv==1.0.0",
        "feedparser==6.0.10",
        "httpx==0.25.1",
        "playwright==1.40.0",
    ],
    entry_points={
        "console_scripts": [
            "scraper-bot=main:main",
        ],
    },
)
