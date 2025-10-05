# -*- coding: utf-8 -*-
from .telegram_bot import send_telegram_message
from .api_football import get_today_matches
import datetime

def run_daily_analysis():
    today = datetime.date.today().strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today})\n\n"
    message += "⚽️ Bugünkü Maçlar:\n"

    try:
        matches = get_today_matches()
        if not matches:
            message += "Bugün maç bulunamadı 😅"
        else:
            for m in matches[:10]:
                message += f"• {m}\n"
    except Exception as e:
        message += f"Hata oluştu: {e}\n"

    message += "\n🔮 Tahminler istatistiklere göre sıralanacak."

    # Türkçe karakter hatalarını önlemek için
    message = message.encode("utf-8", errors="ignore").decode("utf-8")

    send_telegram_message(message)

