# bot.py

# This file should contain bot-specific logic that does NOT depend on the
# FastAPI application instance.
# For example, you could define game logic classes or helper functions here.

# CRITICAL: DO NOT add `from api.main import bot_app` to this file.
# That line was the cause of the circular import error.

# The bot handlers are now configured in bot/handlers.py and initialized by api/main.py.