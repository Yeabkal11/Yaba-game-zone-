# bot/handlers.py (Simplified Web App Launcher)

import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logger = logging.getLogger(__name__)

# This gets your Render URL from the environment variables you already set.
WEB_APP_URL = os.getenv("WEBHOOK_URL")

# --- Define the Keyboard Layout ---
# We are changing ONLY the "Play" button.
main_keyboard = [
    # THIS IS THE ONLY BUTTON WE ARE CHANGING.
    # It now has a `web_app` parameter. When tapped, it will open your new website.
    [KeyboardButton("Play 🎮", web_app=WebAppInfo(url=f"{WEB_APP_URL}/lobby/index.html"))],
    
    # The rest of these buttons will still send text, just like before.
    [KeyboardButton("Register 👤"), KeyboardButton("Deposit 💰")],
    [KeyboardButton("Withdraw 💸"), KeyboardButton("Balance 🏦")],
    [KeyboardButton("Transactions 📜"), KeyboardButton("How To Play 📖")],
    [KeyboardButton("Contact Us 📞"), KeyboardButton("Join Group 📢")],
]
REPLY_MARKUP = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)


# This is the function that runs when you send the /start command.
# It simply shows the keyboard.
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the main menu keyboard with the Web App button."""
    await update.message.reply_text(
        "Welcome to Yeab Game Zone! Tap 'Play' to see open games or manage your account.", 
        reply_markup=REPLY_MARKUP
    )

# This new function will handle messages that come FROM your website.
# For example, when a user clicks a "Join" button inside the web app.
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles data sent back from the Web App."""
    data_str = update.effective_message.web_app_data.data
    logger.info(f"Received data from Web App: {data_str}")
    
    # Check if the data is a "join game" request
    if data_str.startswith("join_game_"):
        game_id = data_str.split('_')[-1]
        await update.message.reply_text(
            f"Joining game #{game_id}...",
            reply_markup=REPLY_MARKUP # Show the main keyboard again
        )
        # TODO: Add your full game joining logic here.

# This function sets up all the handlers.
def setup_handlers(ptb_app: Application) -> Application:
    """Attaches all handlers."""
    # Add the handler for the /start command
    ptb_app.add_handler(CommandHandler("start", start_command))
    
    # Add the special handler that listens for data from our Web App
    ptb_app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    
    # TODO: You can add handlers for the other text buttons (like "Balance") here later.
    
    return ptb_app