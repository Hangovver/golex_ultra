# tools/daily_runner.py
from tools.alt_thesportsdb import get_today_events
from tools.telegram import send_message
import time

def run_and_notify():
    """Analizi çalıştırır ve Telegram’a gönderir"""
    try:
        send_message("🚀 Golex Ultra analiz başladı...")
        print("⚡ Manuel analiz başlatıldı...")

        events = get_today_events()
        if not events:
            send_message("⚠️ Bugün için maç bulunamadı.")
            return

        msg = "📊 *Bugünün Maçları:*\n\n"
        for e in events:
            match = f"⚽ {e['strEvent']} — {e['dateEvent']} {e['strTime']}\n"
            msg += match
            time.sleep(0.5)

        send_message(msg)
        send_message("✅ Analiz tamamlandı ve Telegram’a gönderildi.")
        print("📊 Manuel analiz tamamlandı.")

    except Exception as e:
        err = f"❌ Hata oluştu: {str(e)}"
        print(err)
        send_message(err)
