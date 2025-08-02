from telegram.ext import CommandHandler, CallbackQueryHandler, Application
from .callbacks import start, play_command, join_game

def setup_handlers() -> Application:
    # A placeholder for the actual application setup
    application = Application.builder().token("dummy-token").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play_command))
    application.add_handler(CallbackQueryHandler(join_game, pattern="^join_"))
    return application