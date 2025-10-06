import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
        response = requests.post(url, json=payload, timeout=10)
        print(f"✅ Telegram yanıtı: {response.text}")
        return response.json()
    except Exception as e:
        print(f"⚠️ Telegram gönderim hatası: {e}")


