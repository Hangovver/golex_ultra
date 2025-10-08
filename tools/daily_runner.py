# tools/daily_runner.py
import time
from datetime import date
from tools.alt_apifootball import get_today_events
from tools.predictor import best_pick_for_match
from tools.telegram import send_telegram_message

LIMIT = 60
ADAPT_RATE = 0.8
MIN_LIMIT = 10

def handle_api_error():
    global LIMIT
    new_limit = max(MIN_LIMIT, int(LIMIT * ADAPT_RATE))
    if new_limit < LIMIT:
        LIMIT = new_limit
        print(f"⚠️ Limit düşürüldü → {LIMIT}")

def run_and_notify():
    global LIMIT
    print("⚡ Günlük analiz başlatıldı...")
    send_telegram_message("⚡ Günlük analiz başlatıldı...")

    try:
        matches = get_today_events()
    except Exception as e:
        send_telegram_message(f"⚠️ Maç listesi alınamadı: {e}")
        handle_api_error()
        return

    results = []
    for m in matches[:LIMIT]:
        try:
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            print(f"🔍 {home} vs {away}")

            pick, info = best_pick_for_match(home, away)
            line = f"{home} – {away} → {pick}\n  • Örneklem: Ev({info['samples']['Ev']}), Dep({info['samples']['Dep']})\n"
            line += "  • " + " | ".join([f"{k}:{'✓' if v else '✗'}" for k, v in info["criteria"].items()])
            results.append(line)

            time.sleep(1)

        except Exception as e:
            print(f"⚠️ Analiz hatası ({m}): {e}")
            handle_api_error()
            time.sleep(2)

    if not results:
        send_telegram_message(f"📊 <b>GOLEX Günlük Analiz ({date.today():%d %B %Y})</b>\n\nBugün uygun maç bulunamadı 😅")
    else:
        send_telegram_message(f"📊 <b>GOLEX Günlük Analiz ({date.today():%d %B %Y})</b>\n\n" + "\n".join(results))

    print("✅ Analiz tamamlandı.")
