import datetime
import sys
import io
from .telegram_bot import send_telegram_message
from .api_football import get_today_matches

# UTF-8 çıktısı için ayar (latin-1 hatasını önler)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_daily_analysis():
    today = datetime.date.today().strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today})\n\n"
    message += "⚽️ Bugünkü Maçlar:\n"

    try:
        matches = get_today_matches()
        if not matches:
            message += "Bugün maç bulunamadı 😅"
        else:
            # Maksimum 20 maç göster
            for m in matches[:20]:
                # Her maçı UTF-8 olarak ekle
                safe_match = str(m).encode("utf-8", errors="ignore").decode("utf-8")
                message += f"• {safe_match}\n"

    except Exception as e:
        message += f"Hata oluştu: {e}\n"

    message += "\n🔮 Tahminler istatistiklere göre sıralanacak."

    try:
        print("Telegram mesajı gönderiliyor...")
        send_telegram_message(message)
        print("✅ Telegram mesajı gönderildi.")
    except Exception as e:
        print(f"⚠️ Telegram gönderim hatası: {e}")

