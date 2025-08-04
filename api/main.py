# api/main.py (Final Cleaned-up Version)

import logging
import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from telegram import Update
from telegram.ext import Application
from telegram.error import RetryAfter

from bot.handlers import setup_handlers

# --- Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Environment Variables ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# --- Application Lifespan (Handles Startup and Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup...")
    if bot_app:
        await bot_app.initialize()
        
        if WEBHOOK_URL:
            webhook_full_url = f"{WEBHOOK_URL}/api/telegram/webhook"
            try:
                await bot_app.bot.set_webhook(url=webhook_full_url, allowed_updates=Update.ALL_TYPES)
                logger.info(f"Successfully set webhook to: {webhook_full_url}")
            except RetryAfter as e:
                logger.warning(f"Could not set webhook due to flood control. Another worker likely succeeded. Error: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred while setting webhook: {e}")
        else:
            logger.error("FATAL: WEBHOOK_URL environment variable is not set!")
    
    yield
    
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
# In api/main.py, add this new endpoint:

@app.get("/api/games")
async def get_open_games():
    """
    This endpoint will be called by the web app to fetch all games
    that are currently in the 'lobby' state.
    """
    # --- TODO: Database Logic ---
    # In your real application, you would query your PostgreSQL database here
    # to find all games with a status of 'lobby'.
    # For now, we will return some fake "dummy" data so we can build the frontend.
    dummy_games = [
        {
            "id": 123,
            "creator_name": "Yeab",
            "creator_avatar": "https://i.pravatar.cc/40?u=123", # Placeholder image
            "stake": 50,
            "prize": 90, # 100 total pot - 10% commission
            "current_players": 1,
            "max_players": 2,
        },
        {
            "id": 124,
            "creator_name": "John D.",
            "creator_avatar": "https://i.pravatar.cc/40?u=124",
            "stake": 20,
            "prize": 36, # 40 total pot - 10% commission
            "current_players": 1,
            "max_players": 2,
        }
    ]
    return {"games": dummy_games}
@app.get("/health")
async def health_check():
    return {"status": "healthy"}