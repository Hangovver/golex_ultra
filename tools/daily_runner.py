# tools/daily_runner.py
import time
import requests
from datetime import date
from config import BASE_URL, HEADERS
from tools.telegram import send_telegram_message
from tools.predictor import best_pick_for_match
from tools.alt_apifootball import get_today_events

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
    """Günlük maç analizini çalıştırır ve Telegram’a gönderir."""
    global LIMIT
    print("⚡ Manuel analiz başlatıldı...")
    send_telegram_message("⚡ Günlük analiz başlatıldı...")

    # Maç listesini çek
    try:
        matches = get_today_events()
    except Exception as e:
        print(f"⚠️ Maç listesi alınamadı: {e}")
        handle_api_error()
        send_telegram_message(f"⚠️ Maç listesi alınamadı: {e}")
        return

    results = []
    for i, m in enumerate(matches[:LIMIT]):
        home_team = m.get("home_team")
        away_team = m.get("away_team")

        if not home_team or not away_team:
           
