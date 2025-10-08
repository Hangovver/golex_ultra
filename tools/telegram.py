# tools/telegram.py
import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send_telegram_message(text: str):
    """Telegram’a mesaj gönderir (HTML destekli)"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload, timeout=10)
    if not r.ok:
        print("⚠️ Telegram hata:", r.text)
    else:
        print(f"✅ Telegram yanıtı: {r.text}")
