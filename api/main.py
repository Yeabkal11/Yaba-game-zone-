# api/main.py

import logging
import os
from fastapi import FastAPI, Request, Response, status
from telegram import Update
from telegram.ext import Application

# This is now a clean, one-way import.
from bot.handlers import setup_handlers

# --- Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Definition ---
app = FastAPI(title="Yeab Game Zone API")

# --- Telegram Bot Initialization ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    logger.error("FATAL: TELEGRAM_BOT_TOKEN environment variable is not set!")
    bot_app = None
else:
    # 1. Create the application instance that needs to be configured.
    ptb_application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # 2. Inject the instance into the setup function from the other module.
    bot_app = setup_handlers(ptb_application)
    logger.info("Telegram bot initialized and handlers have been attached.")


# --- API Endpoints ---
@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    if not bot_app:
        return Response(status_code=503)
    try:
        data = await request.json()
        update = Update.de_json(data, bot_app.bot)
        await bot_app.process_update(update)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}")
        return Response(status_code=500)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}