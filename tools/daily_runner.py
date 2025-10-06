import datetime
from .api_football import get_today_matches
from .telegram import send_telegram_message

def run_daily_analysis():
    try:
        today = datetime.date.today().strftime("%d %B %Y")
        print(f"📅 Analiz başlatıldı: {today}")

        matches = get_today_matches()
        if not matches:
            msg = f"📊 GOLEX Günlük Analiz ({today})\n\n⚽️ Bugün maç bulunamadı.\n\n🔮 Yeni analizler yarın yapılacak."
            send_telegram_message(msg)
            print("⚠️ Bugün maç bulunamadı.")
            return

        message = f"📊 GOLEX Günlük Analiz ({today})\n\n⚽️ Bugünkü Maçlar:\n"
        for m in matches[:30]:
            safe_match = str(m).encode("utf-8", errors="ignore").decode("utf-8")
            message += f"• {safe_match}\n"

        message += "\n🔮 Tahminler istatistiklere göre sıralanacak."
        send_telegram_message(message)
        print("✅ Günlük analiz gönderildi.")

    except Exception as e:
        error_msg = f"⚠️ Genel hata: {str(e)}"
        print(error_msg)
        send_telegram_message(error_msg)
