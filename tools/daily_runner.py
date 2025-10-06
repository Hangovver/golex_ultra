import datetime
from .api_football import get_today_matches
from .telegram import send_telegram_message

def run_daily_analysis():
    try:
        today = datetime.date.today().strftime("%d %B %Y")
        print(f"📅 Analiz başlatıldı: {today}")

        matches = get_today_matches()
        if not matches:
            msg = f"📊 GOLEX Günlük Analiz ({today})\n\n⚽️ Bugün için maç bulunamadı veya API boş döndü.\n🔁 Lütfen API anahtarını veya zaman dilimini kontrol et."
            send_telegram_message(msg)
            print("⚠️ Maç bulunamadı.")
            return

        message = f"📊 GOLEX Günlük Analiz ({today})\n\n⚽️ Bugünkü Maçlar:\n"
        for m in matches[:30]:
            message += f"• {m}\n"

        message += "\n🔮 Tahminler istatistiklere göre hazırlanacak."
        send_telegram_message(message)
        print("✅ Günlük analiz Telegram'a gönderildi.")

    except Exception as e:
        error_msg = f"⚠️ Genel hata: {str(e)}"
        print(error_msg)
        send_telegram_message(error_msg)
