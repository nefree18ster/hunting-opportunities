import requests

BOT_TOKEN = '7726784700:AAFjmjVc9NUGYlq0Cmtmh0rEfbf-Di2D4B8'  # Paste from BotFather
CHAT_ID = 'YO502825466'      # From @userinfobot

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
    except Exception as e:
        print("Error sending Telegram alert:", e)
