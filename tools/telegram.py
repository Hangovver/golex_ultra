# tools/telegram.py
import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send_telegram_message(text: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("⚠️ Telegram ayarlı değil.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        print(f"✅ Telegram yanıtı: {r.text}")
    except Exception as e:
        print(f"⚠️ Telegram gönderilemedi: {e}")
