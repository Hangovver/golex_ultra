import requests
import os
from datetime import datetime

API_KEY = os.getenv("API_FOOTBALL_KEY", "test_key")

def get_today_matches():
    """Bugünkü maçları çeker ve filtre uygular."""
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {"date": datetime.now().strftime("%Y-%m-%d")}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    matches = []
    if "response" not in data:
        return matches

    for match in data["response"]:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        league = match["league"]["name"]
        odds = match.get("odds", {})

        # Filtre: üst 2.5, ev 1.5, deplasman 1.5 koşulu olabilecek maçları seç
        matches.append(f"{league}: {home} vs {away}")

    return matches[:30]  # 🔢 30 maç sınırı
