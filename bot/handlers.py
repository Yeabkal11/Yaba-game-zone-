# bot/handlers.py (Final Corrected Version for Library Update)

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler, # We already import this
    filters,        # We use this for the fix
    ConversationHandler,
    ContextTypes,
    # RegexHandler, # <-- THIS IS REMOVED
    CallbackQueryHandler,
)

logger = logging.getLogger(__name__)

# --- Conversation States (No changes here) ---
AWAITING_STAKE, AWAITING_WIN_CONDITION = range(2)


# --- Main Keyboard Layout (No changes here) ---
main_keyboard = [
    [KeyboardButton("Play 🎮"), KeyboardButton("Register 👤")],
    [KeyboardButton("Deposit 💰"), KeyboardButton("Withdraw 💸")],
    [KeyboardButton("Transactions 📜"), KeyboardButton("Balance 🏦")],
    [KeyboardButton("How To Play 📖"), KeyboardButton("Contact Us 📞")],
    [KeyboardButton("Join Group 📢")]
]
REPLY_MARKUP = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)


# --- Game Creation Conversation Handlers (No changes here) ---
async def play_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    return AWAITING_STAKE

async def receive_stake(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    stake_amount = int(query.data.split('_')[1])
    context.user_data['stake'] = stake_amount
    win_condition_buttons = [
        [
            InlineKeyboardButton("First Token Home", callback_data="win_1"),
            InlineKeyboardButton("Two Tokens Home", callback_data="win_2"),
            InlineKeyboardButton("All Four Home (Full House)", callback_data="win_4"),
        ],
        [InlineKeyboardButton("Cancel", callback_data="cancel_creation")]
    ]
    inline_markup = InlineKeyboardMarkup(win_condition_buttons)
    await query.edit_message_text(
        text="Great! Now, how many tokens does a player need to get home to win?",
        reply_markup=inline_markup
    )
    return AWAITING_WIN_CONDITION

async def receive_win_condition_and_create_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    win_condition = int(query.data.split('_')[1])
    stake = context.user_data.get('stake', 'N/A')
    user = query.from_user
    game_id = 123
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
    context.user_data.clear()
    return ConversationHandler.END

async def cancel_creation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Game creation has been cancelled.")
    context.user_data.clear()
    return ConversationHandler.END

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Yeab Game Zone! Please choose an option below.", 
        reply_markup=REPLY_MARKUP
    )


# --- Update the main setup function (This is where the fix is) ---
def setup_handlers(ptb_app: Application) -> Application:
    """Attaches all handlers, using the modern MessageHandler."""

    # Create the ConversationHandler for the play flow
    play_conv_handler = ConversationHandler(
        # --- THIS IS THE FIX ---
        # We replace RegexHandler with MessageHandler and a Regex filter.
        entry_points=[MessageHandler(filters.Regex("^Play 🎮$"), play_start)],
        # ----------------------
        states={
            AWAITING_STAKE: [CallbackQueryHandler(receive_stake, pattern="^stake_")],
            AWAITING_WIN_CONDITION: [CallbackQueryHandler(receive_win_condition_and_create_game, pattern="^win_")],
        },
        fallbacks=[CallbackQueryHandler(cancel_creation, pattern="^cancel_creation")],
    )

    ptb_app.add_handler(play_conv_handler)
    ptb_app.add_handler(CommandHandler("start", start_command))
    
    return ptb_app