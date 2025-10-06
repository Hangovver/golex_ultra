import sys
import os
import io
from datetime import datetime
from .api_football import get_today_matches
from .telegram import send_telegram_message

# UTF-8 uyumluluğu
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="ignore")

def run_daily_analysis():
    try:
        today = datetime.utcnow().strftime("%d %B %Y")
        matches = get_today_matches()

        message = f"📊 GOLEX Günlük Analiz ({today})\n\n"

        if not matches:
            message += "⚽️ Bugünkü maçlar bulunamadı.\n"
        else:
            message += "⚽️ Bugünkü Maçlar ve Tahminler:\n"
            for m in matches:
                safe_match = str(m).encode("utf-8", errors="ignore").decode("utf-8")
                message += f"• {safe_match}\n"

        message += "\n🔮 Tahminler son 5 maç istatistiklerine göre oluşturulmuştur."
        send_telegram_message(message)

    except Exception as e:
        err_msg = f"⚠️ Genel hata: {e}"
        print(err_msg)
        send_telegram_message(f"📊 GOLEX Günlük Analiz Hatası:\n{err_msg}")


