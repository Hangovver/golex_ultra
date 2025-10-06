import requests
from datetime import datetime, timedelta

def get_matches_from_thesportsdb():
    # 🔹 Dünkü tarihi al (UTC+3 saat farkıyla)
    today = (datetime.utcnow() + timedelta(hours=3) - timedelta(days=1)).strftime("%Y-%m-%d")

    # 🔹 TheSportsDB API URL’si
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer"

    try:
        response = requests.get(url)
        data = response.json()

        # 🔹 Maç verisi varsa döndür
        if data.get("events"):
            matches = []
            for event in data["events"]:
                home = event.get("strHomeTeam", "Bilinmiyor")
                away = event.get("strAwayTeam", "Bilinmiyor")
                league = event.get("strLeague", "Bilinmiyor")
                time = event.get("strTime", "Bilinmiyor")
                matches.append(f"{league}: {home} vs {away} ({time})")
            return matches
        else:
            return []

    except Exception as e:
        print("❌ Hata:", e)
        return []
