# bot/handlers.py

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# NOTE: You should create a bot/callbacks.py file to hold your actual logic.
# from .callbacks import start_callback, play_callback, join_game_callback

# --- Placeholder Callbacks (for demonstration) ---
# Replace these with your actual functions in a separate callbacks file.
async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text("Welcome to the Yeab Game Zone Ludo Bot! Use /play to start a new game.")

async def play_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /play command to start game creation."""
    # In your full implementation, you would send inline keyboard buttons here
    # for setting the stake and win condition.
    await update.message.reply_text("Let's create a game! Please choose a stake amount.")


# --- Handler Setup Function ---

def setup_handlers(ptb_app: Application) -> Application:
    """
    Attaches all command and callback query handlers to the python-telegram-bot Application.
    This is the single entry point for registering all bot behaviors.

    Args:
        ptb_app: The Application instance created in api/main.py.

    Returns:
        The same Application instance with all handlers correctly attached.
    """
    # Register your command handlers
    ptb_app.add_handler(CommandHandler("start", start_callback))
    ptb_app.add_handler(CommandHandler("play", play_callback))

    # Register your callback query handlers (for buttons) here
    # Example:
    # ptb_app.add_handler(CallbackQueryHandler(join_game_callback, pattern="^join_game:"))
    
    return ptb_app