# tools/telegram.py
import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send_message_markdown(text: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("ℹ️ Telegram bilgileri eksik; mesaj gönderilmedi.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    r = requests.post(url, json=payload, timeout=20)
    try:
        r.raise_for_status()
        print(f"✅ Telegram yanıtı: {r.text}")
    except Exception as e:
        print(f"⚠️ Telegram gönderim hatası: {e} | {r.text}")
