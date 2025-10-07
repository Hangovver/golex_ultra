# tools/telegram.py
import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send_message(text):
    """Telegram’a mesaj gönderir"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("⚠️ Telegram bilgileri eksik")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        r = requests.post(url, data=data)
        if r.status_code != 200:
            print(f"❌ Telegram hata: {r.text}")
    except Exception as e:
        print(f"❌ Telegram bağlantı hatası: {e}")




