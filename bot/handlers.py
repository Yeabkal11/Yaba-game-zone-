# bot/handlers.py

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# It's good practice to keep your callback logic in a separate file.
# You would need to create bot/callbacks.py and define these functions there.
# from .callbacks import start, play_command, join_game_callback

# For now, here are placeholder callbacks to make the file runnable:
async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text("Welcome to the Yeab Game Zone Ludo Bot!")

async def play_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the game creation flow when /play is issued."""
    # This is where you would send buttons for stake amount and win conditions.
    await update.message.reply_text("Let's create a game! Please choose a stake amount.")


def setup_handlers(ptb_app: Application) -> Application:
    """
    Attaches all command and callback query handlers to the python-telegram-bot Application.
    This function acts as the single entry point for registering all bot behaviors.

    Args:
        ptb_app: The Application instance created in api/main.py.

    Returns:
        The same Application instance with all handlers correctly attached.
    """
    # Register command handlers
    ptb_app.add_handler(CommandHandler("start", start_callback))
    ptb_app.add_handler(CommandHandler("play", play_callback))

    # Register callback query handlers (for inline buttons)
    # Example:
    # ptb_app.add_handler(CallbackQueryHandler(join_game_callback, pattern="^join_game:"))
    
    return ptb_app