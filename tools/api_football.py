import requests
import os
import datetime

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io/"

def get_today_matches():
    """Bugünkü maçları API'den çeker"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    url = f"{BASE_URL}fixtures?date={today}"

    headers = {
        "x-apisports-key": API_KEY
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    matches = []
    if "response" in data:
        for m in data["response"]:
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            league = m["league"]["name"]
            matches.append(f"{home} vs {away} ({league})")

    return matches
