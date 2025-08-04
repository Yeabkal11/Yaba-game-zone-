# bot/handlers.py (Final Game Creation Version)

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
    RegexHandler,
    CallbackQueryHandler,
)

# This gets the same logger that FastAPI uses.
logger = logging.getLogger(__name__)

# --- 1. Define Conversation States ---
# We create states for each step of the game creation process.
AWAITING_STAKE, AWAITING_WIN_CONDITION = range(2)


# --- 2. Define the Main Keyboard Layout ---
main_keyboard = [
    [KeyboardButton("Play 🎮"), KeyboardButton("Register 👤")],
    [KeyboardButton("Deposit 💰"), KeyboardButton("Withdraw 💸")],
    [KeyboardButton("Transactions 📜"), KeyboardButton("Balance 🏦")],
    [KeyboardButton("How To Play 📖"), KeyboardButton("Contact Us 📞")],
    [KeyboardButton("Join Group 📢")]
]
REPLY_MARKUP = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)


# --- 3. Handlers for the Game Creation Conversation ---

# This function is the entry point, triggered by the "Play 🎮" button
async def play_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the game creation process by asking for the stake amount."""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} started the game creation process.")

    # We use Inline Buttons here because they are attached to a message and are better for one-off choices.
    stake_buttons = [
        [
            InlineKeyboardButton("20 ETB", callback_data="stake_20"),
            InlineKeyboardButton("50 ETB", callback_data="stake_50"),
            InlineKeyboardButton("100 ETB", callback_data="stake_100"),
        ],
        [InlineKeyboardButton("Cancel", callback_data="cancel_creation")]
    ]
    inline_markup = InlineKeyboardMarkup(stake_buttons)
    
    await update.message.reply_text(
        "Please select a stake amount for the game:",
        reply_markup=inline_markup
    )
    
    # We are now waiting for the user to tap one of the stake buttons
    return AWAITING_STAKE

# This function runs after the user selects a stake amount
async def receive_stake(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves the stake amount and asks for the winning condition."""
    query = update.callback_query
    await query.answer() # Acknowledge the button tap

    # We use context.user_data to store information during the conversation
    stake_amount = int(query.data.split('_')[1])
    context.user_data['stake'] = stake_amount
    
    logger.info(f"User {query.from_user.id} chose stake: {stake_amount}")

    win_condition_buttons = [
        [
            InlineKeyboardButton("First Token Home", callback_data="win_1"),
            InlineKeyboardButton("Two Tokens Home", callback_data="win_2"),
            InlineKeyboardButton("All Four Home (Full House)", callback_data="win_4"),
        ],
        [InlineKeyboardButton("Cancel", callback_data="cancel_creation")]
    ]
    inline_markup = InlineKeyboardMarkup(win_condition_buttons)

    # We edit the previous message to avoid cluttering the chat
    await query.edit_message_text(
        text="Great! Now, how many tokens does a player need to get home to win?",
        reply_markup=inline_markup
    )

    # We are now waiting for the user to choose a win condition
    return AWAITING_WIN_CONDITION

# This function runs after the user selects the win condition
async def receive_win_condition_and_create_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saves win condition, creates the game lobby, and ends the conversation."""
    query = update.callback_query
    await query.answer()

    win_condition = int(query.data.split('_')[1])
    stake = context.user_data.get('stake', 'N/A') # Retrieve the saved stake
    user = query.from_user

    logger.info(f"User {user.id} chose win condition: {win_condition}. Creating game lobby.")

    # --- TODO: Database Logic Goes Here ---
    # 1. Check if the user has enough balance (stake).
    # 2. Create a new game entry in your 'games' table with status 'lobby'.
    #    - creator_id = user.id
    #    - stake = stake
    #    - win_condition = win_condition
    # 3. Get the new unique 'game_id' from the database.
    game_id = 123 # Using a placeholder for now

    # Create the lobby message with a "Join Game" button
    join_button = [[InlineKeyboardButton("Join Game", callback_data=f"join_{game_id}")]]
    inline_markup = InlineKeyboardMarkup(join_button)

    lobby_message = (
        f"📣 Game Lobby Created!\n\n"
        f"👤 **Creator:** {user.first_name}\n"
        f"💰 **Stake:** {stake} ETB\n"
        f"🏆 **Win Condition:** {win_condition} token(s) home\n\n"
        f"Waiting for an opponent to join..."
    )

    await query.edit_message_text(text=lobby_message, reply_markup=inline_markup)
    
    # Clean up the temporary data
    context.user_data.clear()
    
    # End the conversation
    return ConversationHandler.END

async def cancel_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the game creation process."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Game creation has been cancelled.")
    context.user_data.clear()
    return ConversationHandler.END


# --- 4. The main /start handler (no changes needed) ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the main menu keyboard."""
    await update.message.reply_text(
        "Welcome to Yeab Game Zone! Please choose an option below.", 
        reply_markup=REPLY_MARKUP
    )


# --- 5. Update the main setup function ---
def setup_handlers(ptb_app: Application) -> Application:
    """Attaches all handlers, including the new game creation conversation."""

    # Create the ConversationHandler for the play flow
    play_conv_handler = ConversationHandler(
        entry_points=[RegexHandler("^Play 🎮$", play_start)],
        states={
            AWAITING_STAKE: [CallbackQueryHandler(receive_stake, pattern="^stake_")],
            AWAITING_WIN_CONDITION: [CallbackQueryHandler(receive_win_condition_and_create_game, pattern="^win_")],
        },
        fallbacks=[CallbackQueryHandler(cancel_creation, pattern="^cancel_creation")],
    )

    ptb_app.add_handler(play_conv_handler)
    ptb_app.add_handler(CommandHandler("start", start_command))
    # We remove the old simple handler and replace it with the conversation
    # ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_taps))
    
    return ptb_app