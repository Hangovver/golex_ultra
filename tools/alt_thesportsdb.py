import requests
from datetime import datetime, timedelta
import os

# Türkiye saatine göre bugünün tarihini al
today = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y-%m-%d")

def get_matches():
    """
    TheSportsDB üzerinden bugünkü maçları çeker.
    """
    try:
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer"
        print(f"📅 Maç verisi isteniyor: {url}")
        response = requests.get(url, timeout=10)
        data = response.json()

        # Maç bulunamadıysa
        if not data or not data.get("events"):
            print("⚽️ Bugün için maç bulunamadı.")
            return []

        matches = []
        for event in data["events"]:
            home = event.get("strHomeTeam", "Bilinmiyor")
            away = event.get("strAwayTeam", "Bilinmiyor")
            league = event.get("strLeague", "Bilinmiyor")
            time = event.get("strTime", "Saat Yok")
            matches.append(f"{league}: {home} vs {away} ({time})")

        return matches

    except Exception as e:
        print(f"❌ TheSportsDB bağlantı hatası: {e}")
        return []

# Test amaçlı çalıştırmak istersen:
if __name__ == "__main__":
    matches = get_matches()
    if matches:
        print("\n".join(matches))
    else:
        print("Bugün için maç bulunamadı 😅")
