# tools/daily_runner.py
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

import datetime
from .telegram_bot import send_telegram_message
from .api_football import get_today_matches


def run_daily_analysis():
    """Günlük analiz çalıştırır ve sonucu Telegram'a gönderir."""
    today = datetime.date.today().strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today})\n\n"
    message += "⚽️ Bugünkü Maçlar:\n"

    try:
        matches = get_today_matches()
        if not matches:
            message += "Bugün maç bulunamadı 😅"
        else:
            # İlk 20 maçı listele
            for m in matches[:20]:
                # Her maç satırı güvenli biçimde UTF-8'e dönüştürülür
                safe_match = str(m).encode("utf-8", errors="ignore").decode("utf-8")
                message += f"• {safe_match}\n"
    except Exception as e:
        safe_error = str(e).encode("utf-8", errors="ignore").decode("utf-8")
        message += f"Hata oluştu: {safe_error}\n"

    message += "\n🔮 Tahminler istatistiklere göre sıralanacak."

    # Telegram’a gönder
    print("Telegram mesajı gönderiliyor...")
    send_telegram_message(message)
    print("✅ Telegram’a gönderildi.")
