import os
from dotenv import load_dotenv
import requests

# Load from neh.env instead of default .env
load_dotenv("neh.env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("Failed to send alert:", response.text)
        else:
            print("Alert sent successfully")
    except Exception as e:
        print("Error sending Telegram alert:", e)
