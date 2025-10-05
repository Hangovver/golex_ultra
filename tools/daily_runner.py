import datetime
from .telegram import send_telegram_message
from .api_football import get_today_matches


def run_daily_analysis():
    today = datetime.date.today().strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today})\n\n"
    message += "⚽️ Bugünkü Maçlar ve Tahminler:\n"

    try:
        matches = get_today_matches()
        if not matches:
            message += "Bugün maç bulunamadı 😅"
        else:
            for m in matches:
                safe_match = str(m).encode("utf-8", errors="ignore").decode("utf-8")
                message += f"• {safe_match}\n"
    except Exception as e:
        message += f"Hata: {e}\n"

    message += "\n🔮 Tahminler istatistiklere göre otomatik oluşturuldu."
    send_telegram_message(message)
