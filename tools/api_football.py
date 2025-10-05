import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

def get_today_matches():
    """Bugünkü maçları alır"""
    url = f"{BASE_URL}/fixtures?date=today"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    matches = []
    for match in data.get("response", []):
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        league = match["league"]["name"]
        matches.append(f"{league}: {home} - {away}")
    return matches
