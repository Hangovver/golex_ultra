import os
import requests

def send_telegram_message(message: str):
    """
    Telegram Bot API kullanarak mesaj gönderir.
    """
    try:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not bot_token or not chat_id:
            print("❌ Telegram ortam değişkenleri eksik.")
            return

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            print("✅ Telegram mesajı gönderildi.")
        else:
            print(f"⚠️ Telegram hatası: {response.text}")

    except Exception as e:
        print(f"⚠️ Telegram hata: {e}")
