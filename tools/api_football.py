import requests
from datetime import datetime
import pytz

# ✅ API Anahtarını buraya gir
API_KEY = "BURAYA_API_KEYİNİ_YAZ"
BASE_URL = "https://v3.football.api-sports.io/fixtures"

def get_today_matches():
    """
    API-Football üzerinden bugünkü maçları çeker.
    Türkiye saatine göre tarihi baz alır ve sonuçları listeler.
    """
    try:
        # Türkiye saat dilimi
        tz = pytz.timezone("Europe/Istanbul")
        today = datetime.now(tz).strftime("%Y-%m-%d")

        # API isteği
        url = f"{BASE_URL}?date={today}"
        headers = {"x-apisports-key": API_KEY}

        print("=" * 60)
        print(f"🕒 API Tarihi (Europe/Istanbul): {today}")
        print(f"📡 API URL: {url}")

        response = requests.get(url, headers=headers)
        print(f"📬 Status Kodu: {response.status_code}")

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.text}")
            return []

        data = response.json()

        # JSON cevabının ilk 500 karakterini göster
        print("✅ API cevabı (ilk 500 karakter):")
        print(str(data)[:500])

        # Gelen response içinde maçları listele
        matches = []
        for item in data.get("response", []):
            fixture = item.get("fixture", {})
            league = item.get("league", {}).get("name", "Bilinmeyen Lig")
            home = item.get("teams", {}).get("home", {}).get("name", "Ev Sahibi")
            away = item.get("teams", {}).get("away", {}).get("name", "Deplasman")
            time = fixture.get("date", "00:00")[11:16]

            matches.append(f"{league}: {home} vs {away} ({time})")

        print(f"🎯 Bulunan maç sayısı: {len(matches)}")
        print("=" * 60)

        return matches

    except Exception as e:
        print(f"🚨 Genel hata: {e}")
        return []
