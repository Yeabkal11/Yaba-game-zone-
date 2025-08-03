# api/main.py

import logging
import os
from fastapi import FastAPI, Request, Response, status
from telegram import Update
from telegram.ext import Application

# Import the setup function from bot.handlers
from bot.handlers import setup_handlers

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- FastAPI App Definition ---
app = FastAPI(
    title="Yeab Game Zone API",
    description="Handles webhooks for the Ludo Telegram Bot.",
    version="1.0.0"
)

# --- Telegram Bot Initialization ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    logger.error("FATAL: TELEGRAM_BOT_TOKEN environment variable is not set!")
    # bot_app will be None, and the webhook will fail gracefully.
    bot_app = None
else:
    # 1. Create the python-telegram-bot Application instance
    ptb_app_builder = Application.builder().token(TELEGRAM_BOT_TOKEN)
    ptb_app = ptb_app_builder.build()

    # 2. Pass the instance to your setup function to attach handlers
    bot_app = setup_handlers(ptb_app)
    logger.info("Telegram bot application initialized and handlers attached.")


# --- API Endpoints ---

@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    """
    Main endpoint to receive updates from Telegram. It passes the update to the
    fully configured python-telegram-bot instance for processing.
    """
    if not bot_app:
        logger.error("Cannot process Telegram update: Bot application not initialized.")
        return Response(status_code=503, content="Service Unavailable: Bot not configured")

    try:
        data = await request.json()
        update = Update.de_json(data, bot_app.bot)
        await bot_app.process_update(update)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}")
        return Response(status_code=500, content="Internal Server Error")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """

    A simple health check endpoint that Render uses to verify that the
    web service is live and responsive.
    """
    return {"status": "healthy", "message": "API service is running."}

# Add other webhook endpoints (like /api/chapa/callback) here if needed