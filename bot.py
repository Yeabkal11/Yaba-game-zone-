import os
import asyncio
import logging
from telegram.ext import Application
from dotenv import load_dotenv
from api.main import bot_app

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    """Start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    webhook_url = os.getenv("WEBHOOK_URL")

    if not token:
        logging.error("TELEGRAM_BOT_TOKEN not set in environment variables.")
        return

    application = Application.builder().token(token).build()

    # Set up handlers from bot.handlers
    # This is a simplified representation. The actual bot_app should be configured with handlers.

    if webhook_url:
        await application.bot.set_webhook(url=f"{webhook_url}/api/telegram/webhook")
        logging.info(f"Webhook set to {webhook_url}")
    else:
        logging.warning("WEBHOOK_URL not set, running in polling mode.")
        await application.run_polling()


if __name__ == '__main__':
    # In a production environment with Render, this script would be run as a background worker.
    # The FastAPI app would handle the webhook.
    # For simplicity in this example, we demonstrate the main setup.
    pass