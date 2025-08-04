# bot/handlers.py (New Version with Reply Keyboard)

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# This gets the same logger that FastAPI uses.
logger = logging.getLogger(__name__)

# --- 1. Define the Keyboard Layout ---
# This creates the grid of buttons you see in the screenshot.
# Emojis are used to match the professional style.
main_keyboard = [
    [KeyboardButton("Play 🎮"), KeyboardButton("Register 👤")],
    [KeyboardButton("Deposit 💰"), KeyboardButton("Withdraw 💸")],
    [KeyboardButton("Transactions 📜"), KeyboardButton("Balance 🏦")],
    [KeyboardButton("How To Play 📖"), KeyboardButton("Contact Us 📞")],
    [KeyboardButton("Join Group 📢")]
]
REPLY_MARKUP = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)


# --- 2. Update the /start command handler ---
# When the bot starts, it will send the welcome message AND the custom keyboard.
async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command and displays the main menu keyboard."""
    user_id = update.effective_user.id
    logger.info(f"Received /start command from user {user_id}")
    try:
        welcome_message = "Welcome to Yeab Game Zone! Please choose an option below."
        await update.message.reply_text(welcome_message, reply_markup=REPLY_MARKUP)
        logger.info(f"Successfully sent welcome message and keyboard to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send /start reply to user {user_id}. Error: {e}", exc_info=True)


# --- 3. Create a handler for ALL button taps ---
# This single function will listen for the text from the buttons.
async def handle_button_taps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all incoming text messages from the reply keyboard."""
    user_id = update.effective_user.id
    text = update.message.text
    logger.info(f"Received text message from {user_id}: '{text}'")

    # This is where you will add the logic for each button.
    # We use if/elif to figure out which button was tapped.
    if text == "Play 🎮":
        # TODO: Add your game creation logic here
        await update.message.reply_text("Let's create a game!")
    
    elif text == "Register 👤":
        # TODO: Add user registration logic
        await update.message.reply_text("You are now registered!")

    elif text == "Deposit 💰":
        # TODO: Add Chapa deposit logic
        await update.message.reply_text("To deposit, please send the amount.")

    elif text == "Withdraw 💸":
        # TODO: Add withdrawal logic
        await update.message.reply_text("To withdraw, please send the amount.")

    elif text == "Balance 🏦":
        # TODO: Add logic to fetch and display user balance
        await update.message.reply_text("Fetching your balance...")

    elif text == "Transactions 📜":
        # TODO: Add logic to show transaction history
        await update.message.reply_text("Here are your recent transactions...")

    # You can add the other buttons here as needed
    else:
        await update.message.reply_text("I'm sorry, I don't understand that command.")


# --- 4. Update the main setup function ---
def setup_handlers(ptb_app: Application) -> Application:
    """Attaches all command and message handlers to the application."""
    # This handler is for the /start command
    ptb_app.add_handler(CommandHandler("start", start_callback))

    # This handler is for ALL text messages that are NOT commands.
    # It will be triggered by our new keyboard buttons.
    ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_taps))
    
    return ptb_app