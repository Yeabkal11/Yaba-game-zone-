# api/main.py (Final, Resilient Version)

import logging
import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from telegram import Update
from telegram.ext import Application
from telegram.error import RetryAfter  # <-- Import the specific error

# --- Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Environment Variables ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# --- Application Lifespan (Handles Startup and Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This block runs on STARTUP
    logger.info("Application startup...")
    if bot_app:
        await bot_app.initialize()
        
        if WEBHOOK_URL:
            webhook_full_url = f"{WEBHOOK_URL}/api/telegram/webhook"
            try:
                # Attempt to set the webhook
                await bot_app.bot.set_webhook(url=webhook_full_url)
                logger.info(f"Successfully set webhook to: {webhook_full_url}")
            
            except RetryAfter as e:
                # CRITICAL FIX: This is an expected error in a multi-worker environment.
                # We log it as a warning, not a crash, because another worker already succeeded.
                logger.warning(f"Could not set webhook due to flood control. Another worker likely succeeded. Error: {e}")
            
            except Exception as e:
                # Catch any other unexpected errors
                logger.error(f"An unexpected error occurred while setting webhook: {e}")
        else:
            logger.error("FATAL: WEBHOOK_URL environment variable is not set!")
    
    yield # The application runs here
    
    # This block runs on SHUTDOWN
    logger.info("Application shutdown...")
    if bot_app:
        await bot_app.shutdown()


# --- Main Application Initialization ---
app = FastAPI(title="Yeab Game Zone API", lifespan=lifespan)
bot_app: Application | None = None

if not TELEGRAM_BOT_TOKEN:
    logger.error("FATAL: TELEGRAM_BOT_TOKEN is not set! Bot will be disabled.")
else:
    ptb_application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    bot_app = setup_handlers(ptb_application)
    logger.info("Telegram bot application created and handlers have been attached.")


# --- API Endpoints ---
@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    if not bot_app:
        return Response(status_code=503)
    try:
        data = await request.json()
        update = Update.de_json(data, bot_app.bot)
        await bot_app.process_update(update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}", exc_info=True)
        return Response(status_code=500)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}