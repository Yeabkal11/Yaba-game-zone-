# api/main.py (Final Version)

import logging
import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from telegram import Update
from telegram.ext import Application

# This is the one-way import that is correct
from bot.handlers import setup_handlers

# --- Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Environment Variables ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # We get this from render.yaml

# --- Webhook Setting Function ---
async def set_webhook(bot_app: Application):
    """
    Sets the Telegram webhook to the URL provided by Render.
    This runs only once when the application starts.
    """
    if not WEBHOOK_URL:
        logger.error("FATAL: WEBHOOK_URL environment variable is not set!")
        return

    webhook_full_url = f"{WEBHOOK_URL}/api/telegram/webhook"
    try:
        await bot_app.bot.set_webhook(url=webhook_full_url)
        logger.info(f"Successfully set webhook to: {webhook_full_url}")
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")


# --- Application Lifespan (Startup and Shutdown Events) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This block runs on STARTUP
    logger.info("Application startup...")
    if bot_app:
        # We run the webhook setup in the background so it doesn't block the server
        asyncio.create_task(set_webhook(bot_app))
    
    yield # The application runs here
    
    # This block runs on SHUTDOWN (optional)
    logger.info("Application shutdown...")


# --- Main Application Initialization ---
app = FastAPI(title="Yeab Game Zone API", lifespan=lifespan)
bot_app: Application | None = None

if not TELEGRAM_BOT_TOKEN:
    logger.error("FATAL: TELEGRAM_BOT_TOKEN is not set! Bot will be disabled.")
else:
    # Initialize the bot and attach handlers
    ptb_application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
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
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}")
        return Response(status_code=500)

@app.get("/health")
async def health_check():
    """This endpoint is used by Render for health checks."""
    return {"status": "healthy"}