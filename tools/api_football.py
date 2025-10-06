import requests
import datetime
import os

# ⚽ API-Football ayarları
API_KEY = os.getenv("API_FOOTBALL_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

def get_today_matches():
    today = datetime.date.today().strftime("%Y-%m-%d")
    print(f"📅 Maçlar çekiliyor: {today}")

    params = {
        "date": today,
        "timezone": "Europe/Istanbul"
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=20)
        response.encoding = "utf-8"

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.status_code} - {response.text}")
            return []

        data = response.json()
        matches = data.get("response", [])

        if not matches:
            print("⚠️ Bugün için maç bulunamadı (API boş döndü).")
            return []

        results = []
        for match in matches:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            league = match["league"]["name"]
            hour = match["fixture"]["date"][11:16]
            results.append(f"{league}: {home} vs {away} ({hour})")

        print(f"✅ {len(results)} maç bulundu.")
        return results

    except Exception as e:
        print(f"⚠️ API isteği başarısız: {e}")
        return []
