# tools/daily_runner.py
import time
import requests
from datetime import date
from config import BASE_URL
from tools.telegram import send_telegram_message
from tools.analyzer import (
    meets_home_1_5,
    meets_away_1_5,
    meets_btts_pair,
    meets_over25_pair,
    meets_btts_over25_pair,
)

LIMIT = 60        # başlangıç üst limit
ADAPT_RATE = 0.8  # hata olursa %20 azalt
MIN_LIMIT = 10    # fazla düşmesin

def handle_api_error():
    global LIMIT
    new_limit = max(MIN_LIMIT, int(LIMIT * ADAPT_RATE))
    if new_limit < LIMIT:
        LIMIT = new_limit
        print(f"⚠️ Limit düşürüldü → {LIMIT}")

def _get_today_events():
    today = date.today().isoformat()
    url = f"{BASE_URL}/eventsday.php"
    params = {"d": today, "s": "Soccer"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("events") or []

def run_and_notify():
    global LIMIT
    print("⚡ Manuel analiz başlatıldı...")
    send_telegram_message("⚡ Günlük analiz başlatıldı...")

    # Maç listesini çek
    try:
        matches = _get_today_events()
    except Exception as e:
        print(f"⚠️ Maç listesi alınamadı: {e}")
        handle_api_error()
        send_telegram_message(f"⚠️ Maç listesi alınamadı: {e}")
        return

    results = []
    for i, m in enumerate(matches[:LIMIT]):
        home_id = m.get("idHomeTeam")
        away_id = m.get("idAwayTeam")
        if not home_id or not away_id:
            continue

        # Rate-limit dostu yavaşlatma
        time.sleep(0.6)

        try:
            # Öncelik sırasına göre ilk uygun tahmini seç
            if meets_home_1_5(home_id):
                pick = "🏠 Ev 1.5 Üst"
            elif meets_away_1_5(away_id):
                pick = "🚗 Dep 1.5 Üst"
            elif meets_btts_pair(home_id, away_id):
                pick = "⚽ KG Var"
            elif meets_over25_pair(home_id, away_id):
                pick = "🔥 2.5 Üst"
            elif meets_btts_over25_pair(home_id, away_id):
                pick = "💥 KG + 2.5"
            else:
                pick = None

            if pick:
                results.append(f"{m.get('strEvent')} → {pick}")

        except requests.HTTPError as e:
            # 429 vs.
            print(f"⚠️ API hatası: {e}")
            handle_api_error()
            # çok yüklenmeyelim
            time.sleep(2)
            continue
        except Exception as e:
            print(f"⚠️ Analiz hatası: {e}")
            # devam

    # Sonuçları gönder
    if not results:
        send_telegram_message(
            f"📊 <b>GOLEX Günlük Analiz ({date.today().strftime('%d %B %Y')})</b>\n\n"
            f"Bugün uygun maç bulunamadı 😅"
        )
    else:
        text = "📊 <b>GOLEX Günlük Analiz ({})</b>\n\n{}".format(
            date.today().strftime('%d %B %Y'),
            "\n".join(results)
        )
        send_telegram_message(text)

    print("✅ Analiz tamamlandı, Telegram’a gönderildi.")
