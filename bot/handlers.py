# bot/handlers.py

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Placeholder Callbacks ---
# (You should create a bot/callbacks.py file for these)
async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await update.message.reply_text("Welcome to the Yeab Game Zone!")

async def play_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /play command."""
    await update.message.reply_text("Let's create a game!")


# --- Handler Setup Function (Dependency Injection) ---
def setup_handlers(ptb_app: Application) -> Application:
    """
    This function accepts the `python-telegram-bot` Application instance
    as an argument, breaking the circular import. This is dependency injection.
    """
    # Register all your handlers here
    ptb_app.add_handler(CommandHandler("start", start_callback))
    ptb_app.add_handler(CommandHandler("play", play_callback))
    
    return ptb_app