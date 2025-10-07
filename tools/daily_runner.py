# tools/daily_runner.py
import requests, time
from datetime import date
from config import BASE_URL
from tools.analyzer import analyze_team_stats
from tools.telegram import send_telegram_message

LIMIT = 60  # Başlangıçta maksimum maç sayısı
ADAPT_RATE = 0.8  # API limitine takılırsa %20 azalt

def get_today_matches():
    today = date.today().isoformat()
    url = f"{BASE_URL}/eventsday.php?d={today}&s=Soccer"
    r = requests.get(url, timeout=10)
    data = r.json().get("events", [])
    return data or []

def run_and_notify():
    global LIMIT
    print("⚡ Manuel analiz başlatıldı...")
    send_telegram_message("⚡ Günlük analiz başlatıldı...")

    try:
        matches = get_today_matches()
    except Exception as e:
        print(f"⚠️ Maç listesi alınamadı: {e}")
        send_telegram_message(f"⚠️ Maç listesi alınamadı: {e}")
        return

    results = []
    for i, m in enumerate(matches[:LIMIT]):
        home_id, away_id = m.get("idHomeTeam"), m.get("idAwayTeam")
        if not home_id or not away_id:
            continue

        time.sleep(0.5)

        # Tahmin sırası — uygun olan ilkini seç
        predictions = {
            "🏠 Ev 1.5 Üst": analyze_team_stats(home_id, "home_1.5"),
            "🚗 Dep 1.5 Üst": analyze_team_stats(away_id, "away_1.5"),
            "⚽ KG Var": analyze_team_stats(home_id, "btts"),
            "🔥 2.5 Üst": analyze_team_stats(home_id, "over_2.5"),
            "💥 KG + 2.5": analyze_team_stats(home_id, "btts_2.5"),
        }

        for label, ok in predictions.items():
            if ok:
                results.append(f"{m['strEvent']} → {label}")
                break

    # Eğer sonuç yoksa
    if not results:
        send_telegram_message(f"📊 GOLEX Günlük Analiz ({date.today().strftime('%d %B %Y')})\n\nBugün uygun maç bulunamadı 😅")
    else:
        text = f"📊 <b>GOLEX Günlük Analiz ({date.today().strftime('%d %B %Y')})</b>\n\n" + "\n".join(results)
        send_telegram_message(text)

    print("✅ Analiz tamamlandı, Telegram’a gönderildi.")

# Limit düşürme mantığı (AI Adaptation)
def handle_api_error():
    global LIMIT
    LIMIT = int(LIMIT * ADAPT_RATE)
    print(f"⚠️ Limit düşürüldü → {LIMIT}")
