"""
Main Bot Telegram - Super Scraper Bot
"""
import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ConversationHandler
)
from config import TELEGRAM_TOKEN, BOT_NAME, BOT_VERSION
from handlers import (
    start, help_command, get_news, get_quote, 
    get_crypto, get_weather, scrape_url, 
    scrape_table, scrape_links, unknown_command
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot"""
    
    logger.info(f"🤖 Starting {BOT_NAME} v{BOT_VERSION}")
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("news", get_news))
    application.add_handler(CommandHandler("quote", get_quote))
    application.add_handler(CommandHandler("crypto", get_crypto))
    application.add_handler(CommandHandler("weather", get_weather))
    application.add_handler(CommandHandler("scrape", scrape_url))
    application.add_handler(CommandHandler("table", scrape_table))
    application.add_handler(CommandHandler("links", scrape_links))
    
    # Register unknown command handler
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # Start bot
    logger.info("🚀 Bot is running!")
    logger.info(f"📝 To stop the bot, press Ctrl+C")
    
    application.run_polling(allowed_updates=['message', 'edited_message'])


if __name__ == '__main__':
    main()
