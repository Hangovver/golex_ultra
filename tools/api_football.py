import requests
import datetime
import os

# API-Football ayarları
API_KEY = os.getenv("API_FOOTBALL_KEY", "YOUR_API_KEY_HERE")  # Render Environment'da ekle
BASE_URL = "https://v3.football.api-sports.io/fixtures"

headers = {
    "x-apisports-key": API_KEY
}

def get_today_matches():
    today = datetime.date.today().strftime("%Y-%m-%d")
    params = {"date": today, "timezone": "Europe/Istanbul"}
    print(f"📅 Maçlar çekiliyor: {today}")

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=15)
        response.encoding = "utf-8"

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.status_code}")
            return []

        data = response.json()
        matches = data.get("response", [])

        if not matches:
            print("⚠️ Bugün için maç verisi bulunamadı.")
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
