# tools/alt_apifootball.py
import os
import requests
from datetime import date

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

def get_today_events():
    """Bugünkü futbol maçlarını getirir"""
    today = date.today().isoformat()
    url = f"{BASE_URL}/fixtures"
    params = {"date": today}
    r = requests.get(url, headers=HEADERS, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("response", [])

def get_team_id(team_name):
    """Takım adından API-Football ID'si döndürür"""
    url = f"{BASE_URL}/teams"
    params = {"search": team_name}
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    r.raise_for_status()
    res = r.json().get("response", [])
    if not res:
        raise ValueError(f"Takım bulunamadı: {team_name}")
    return res[0]["team"]["id"]

def get_last_matches(team_name, side=None):
    """Son 5 maçı döndürür. side: 'home' veya 'away'"""
    team_id = get_team_id(team_name)
    url = f"{BASE_URL}/fixtures"
    params = {"team": team_id, "last": 10}
    r = requests.get(url, headers=HEADERS, params=params, timeout=20)
    r.raise_for_status()
    matches = r.json().get("response", [])

    result = []
    for m in matches:
        fixture = m.get("fixture", {})
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        gh, ga = m["goals"]["home"], m["goals"]["away"]

        if side == "home" and m["teams"]["home"]["id"] != team_id:
            continue
        if side == "away" and m["teams"]["away"]["id"] != team_id:
            continue

        result.append({
            "date": fixture.get("date"),
            "homeTeam": home,
            "awayTeam": away,
            "homeGoals": gh,
            "awayGoals": ga,
        })
        if len(result) >= 5:
            break

    return result
