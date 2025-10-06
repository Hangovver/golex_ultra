from .api_football import get_today_matches
from .telegram import send_telegram_message
import datetime

def run_daily_analysis():
    today = datetime.date.today().strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today})\n\n"
    message += "⚽️ Bugünkü Maçlar:\n"

    try:
        matches = get_today_matches()
        if not matches or matches == ["Bugün için maç bulunamadı."]:
            message += "• Bugün için maç bulunamadı 😅\n"
        else:
            for m in matches[:30]:
                safe_match = str(m).encode("utf-8", errors="ignore").decode("utf-8")
                message += f"• {safe_match}\n"
    except Exception as e:
        message += f"⚠️ Hata oluştu: {e}\n"

    message += "\n🔮 Tahminler istatistiklere göre sıralanacak."
    send_telegram_message(message)
