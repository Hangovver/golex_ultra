import datetime
import sys
import io
from .telegram import send_telegram_message
from .api_football import get_today_matches

# --- UTF-8 fix for Render environment ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def run_daily_analysis():
    today = datetime.date.today().strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today})\n\n"
    message += "⚽️ Bugünkü Maçlar:\n"

    try:
        matches = get_today_matches()

        if not matches:
            message += "Bugün maç bulunamadı 😅"
        else:
            # İlk 30 maçı listele
            for m in matches[:30]:
                # Türkçe karakter sorunlarını önlemek için UTF-8 dönüşümü
                safe_match = str(m).encode("utf-8", errors="replace").decode("utf-8")
                message += f"• {safe_match}\n"

    except Exception as e:
        message += f"Hata oluştu: {e}\n"

    message += "\n🔮 Tahminler istatistiklere göre sıralanacak."

    try:
        send_telegram_message(message)
    except Exception as e:
        print(f"⚠️ Telegram gönderim hatası: {e}")

