import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    """Telegram mesajı gönderir (UTF-8 güvenli)"""
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Telegram ayarları eksik! BOT_TOKEN veya CHAT_ID tanımlanmadı.")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text.encode("utf-8", errors="ignore").decode("utf-8"),
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)
    if not response.ok:
        raise Exception(f"Telegram hata: {response.text}")
