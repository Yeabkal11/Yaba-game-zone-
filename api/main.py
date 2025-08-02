import logging
import os
from fastapi import FastAPI, Request, Response, status, Depends
from telegram import Update
from telegram.ext import Application
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

# Adjust these import paths to match your final project structure
from bot.handlers import setup_handlers
from bot.wallet import verify_transaction
from database_models.manager import get_db_session, transactions, users

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- FastAPI App and Telegram Bot Initialization ---
app = FastAPI(
    title="Yeab Game Zone API",
    description="Handles webhooks for the Ludo Telegram Bot.",
    version="1.0.0"
)

# Initialize the python-telegram-bot application instance.
# The webhook itself will be set by a separate startup process.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    logger.error("FATAL: TELEGRAM_BOT_TOKEN environment variable is not set!")
    # This will prevent the bot from working, but the API will still start
    # to allow for health checks and other potential endpoints.
    bot_app = None
else:
    # This sets up all your command and callback handlers from bot/handlers.py
    ptb_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    bot_app = setup_handlers(ptb_app)


# --- API Endpoints ---

@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    """
    This is the main endpoint to receive updates from Telegram's webhook.
    It passes the update to the python-telegram-bot instance for processing.
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


@app.post("/api/chapa/callback")
async def chapa_callback(request: Request, db: AsyncSession = Depends(get_db_session)):
    """
    This endpoint receives server-to-server notifications from the Chapa payment gateway.
    """
    try:
        data = await request.json()
        tx_ref = data.get("tx_ref")
        logger.info(f"Received Chapa callback for tx_ref: {tx_ref}")

        if tx_ref and await verify_transaction(tx_ref):
            logger.info(f"Chapa transaction successfully verified for tx_ref: {tx_ref}")
            #
            # TODO: Add your database logic here to credit the user's wallet
            # 1. Find the transaction in your 'transactions' table via tx_ref
            # 2. Check if its status is 'pending'
            # 3. Calculate the credited amount (amount - 2% fee)
            # 4. Update the user's balance in the 'users' table
            # 5. Set the transaction status to 'completed'
            #
            pass # Placeholder for the logic described above

        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error processing Chapa callback: {e}")
        return Response(status_code=500, content="Internal Server Error")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    A simple health check endpoint that Render uses to verify that the
    web service is live and responsive.
    """
    return {"status": "healthy", "message": "API service is running."}