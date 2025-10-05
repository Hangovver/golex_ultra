import requests
import datetime
import os

# API Football ayarları
API_KEY = os.getenv("FOOTBALL_API_KEY", "BURAYA_API_KEYİNİ_YAZ")
BASE_URL = "https://v3.football.api-sports.io"

# Bugünkü maçları çeken fonksiyon
def get_today_matches():
    today = datetime.date.today().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/fixtures?date={today}"

    headers = {
        "x-apisports-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        matches = []
        for match in data.get("response", []):
            teams = match["teams"]
            home = teams["home"]["name"]
            away = teams["away"]["name"]
            league = match["league"]["name"]
            time = match["fixture"]["date"][11:16]  # sadece saat kısmı
            matches.append(f"{time} — {home} vs {away} ({league})")

        return matches
    except Exception as e:
        print("⚠️ Hata (API-Football):", e)
        return []
