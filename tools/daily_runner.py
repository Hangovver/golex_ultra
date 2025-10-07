# tools/daily_runner.py
from tools.alt_thesportsdb import get_today_events
from tools.telegram import send_message
import time

def run_and_notify():
    """Günlük analizi çalıştırır ve Telegram’a yollar"""
    try:
        send_message("🚀 Golex Ultra — Günlük analiz başlıyor...")
        print("⚡ Manuel analiz başlatıldı...")

        events = get_today_events()
        if not events:
            send_message("⚠️ Bugün için maç bulunamadı veya limit düşürülüyor.")
            return

        msg = "📊 *Bugünün Maçları:*\n\n"
        for e in events:
            match = f"⚽ {e['strEvent']} — {e['dateEvent']} {e['strTime']}\n"
            msg += match
            time.sleep(0.4)

        send_message(msg)
        send_message("✅ Günlük analiz tamamlandı.")
        print("📊 Analiz tamamlandı.")

    except Exception as e:
        err = f"❌ Hata oluştu: {str(e)}"
        print(err)
        send_message(err)
