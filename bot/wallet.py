import os
import requests
from decimal import Decimal

CHAPA_API_KEY = os.getenv("CHAPA_API_KEY")
CHAPA_API_URL = "https://api.chapa.co/v1"

def initiate_deposit(user_id: int, amount: Decimal, tx_ref: str) -> str:
    headers = {
        "Authorization": f"Bearer {CHAPA_API_KEY}",
    }
    payload = {
        "amount": str(amount),
        "currency": "ETB",
        "email": "user@example.com",  # Placeholder
        "first_name": "Player",  # Placeholder
        "last_name": str(user_id),
        "tx_ref": tx_ref,
        "callback_url": f"{os.getenv('WEBHOOK_URL')}/api/chapa/callback",
        "return_url": f"https://t.me/{os.getenv('BOT_USERNAME')}",
    }
    response = requests.post(f"{CHAPA_API_URL}/transaction/initialize", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['data']['checkout_url']

def verify_transaction(tx_ref: str) -> bool:
    headers = {
        "Authorization": f"Bearer {CHAPA_API_KEY}",
    }
    response = requests.get(f"{CHAPA_API_URL}/transaction/verify/{tx_ref}", headers=headers)
    if response.status_code == 200:
        return response.json()['status'] == 'success'
    return False