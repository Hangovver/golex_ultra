import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text: str):
    """Telegram mesajı gönderir (UTF-8 uyumlu)"""
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID ayarlanmamış!")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)
    print("Telegram mesajı gönderiliyor...")
    if response.ok:
        print(f"✅ Telegram yanıtı: {response.text}")
    else:
        print(f"❌ Telegram hata: {response.text}")
