from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Yeab Game Zone Ludo Bot!")

async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Logic to create a new game
    pass

async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Logic for a player to join a game
    pass