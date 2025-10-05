# -*- coding: utf-8 -*-
import datetime
from .telegram import send_telegram_message
from .api_football import get_today_matches

def run_daily_analysis():
    """Günlük maç analizini çalıştırır ve Telegram’a gönderir."""
    today = datetime.date.today().strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today})\n\n"
    message += "⚽️ Bugünkü Maçlar:\n"

    try:
        matches = get_today_matches()
        if not matches:
            message += "Bugün maç bulunamadı 😅"
        else:
            # 🔥 Artık 20 maça kadar listeleyecek
            for m in matches[:20]:
                message += f"• {m}\n"
    except Exception as e:
        message += f"Hata oluştu: {e}\n"

    message += "\n🔮 Tahminler istatistiklere göre sıralanacak."

    try:
        send_telegram_message(message)
        print("✅ Telegram mesajı başarıyla gönderildi.")
    except Exception as e:
        print(f"⚠️ Telegram mesajı gönderilirken hata: {e}")


