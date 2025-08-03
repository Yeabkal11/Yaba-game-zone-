# check_webhook.py

import os
import requests
from dotenv import load_dotenv

# --- Setup ---
# This loads the TELEGRAM_BOT_TOKEN from your .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not found.")
    print("Please create a file named .env and add the line: TELEGRAM_BOT_TOKEN='YOUR_TOKEN_HERE'")
else:
    # This is the Telegram API method to get webhook info
    url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
    
    print("--- Asking Telegram for webhook info... ---")
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("ok"):
            result = data.get("result", {})
            webhook_url = result.get("url", "Not Set")
            last_error = result.get("last_error_message", "None")
            
            print("\n--- Webhook Status ---")
            print(f"URL: {webhook_url}")
            print(f"Last Error Message: {last_error}")
            print("------------------------\n")
            
            if not webhook_url:
                print(">>> DIAGNOSIS: The webhook is NOT SET. The bot will not receive messages.")
            else:
                print(">>> DIAGNOSIS: The webhook is set. Check if the URL is correct and if there is a 'Last Error Message'.")

    except Exception as e:
        print(f"An error occurred: {e}")