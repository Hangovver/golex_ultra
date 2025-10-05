import os
import requests

def send_telegram_message(message):
    print("Telegram mesajı gönderiliyor...")  # Log ekledik

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Telegram ayarları eksik")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=data)
        print("✅ Telegram yanıtı:", response.text)
    except Exception as e:
        print("🚨 Telegram hatası:", e)
