# tools/alt_apifootball.py
import os
import requests
from datetime import date

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {"x-apisports-key": API_KEY}

# --- GÜNÜN MAÇLARI ---
def get_today_events():
    """Bugünün tüm futbol maçlarını döndürür"""
    today = date.today().isoformat()
    url = f"{BASE_URL}/fixtures"
    params = {"date": today}
    r = requests.get(url, headers=HEADERS, params=params, timeout=20)
    r.raise_for_status()
    data = r.json().get("response", [])
    return data

# --- TAKIM ID AL ---
def get_team_id(team_name):
    """Takım adından API-Football ID'sini bulur"""
    url = f"{BASE_URL}/teams"
    params = {"search": team_name}
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    r.raise_for_status()
    res = r.json().get("response", [])
    if not res:
        raise ValueError(f"Takım bulunamadı: {team_name}")
    return res[0]["team"]["id"]

# --- SON 5 MAÇ ---
def get_last_matches(team_name, side=None):
    """
    Takımın son 5 maçını döndürür.
    side: 'home' veya 'away' -> filtre
    """
    team_id = get_team_id(team_name)
    url = f"{BASE_URL}/fixtures"
    params = {"team": team_id, "last": 10}  # 10 çek, biz 5 alırız
    r = requests.get(url, headers=HEADERS, params=params, timeout=20)
    r.raise_for_status()
    matches = r.json().get("response", [])

    result = []
    for m in matches:
        fixture = m.get("fixture", {})
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        goals_home = m["goals"]["home"]
        goals_away = m["goals"]["away"]

        # ev/deplasman filtresi
        if side == "home" and m["teams"]["home"]["id"] != team_id:
            continue
        if side == "away" and m["teams"]["away"]["id"] != team_id:
            continue

        result.append({
            "date": fixture.get("date"),
            "homeTeam": home,
            "awayTeam": away,
            "homeGoals": goals_home,
            "awayGoals": goals_away,
        })
        if len(result) >= 5:
            break

    return result

# --- TEST ---
if __name__ == "__main__":
    print("Test Real Madrid son 5 ev maçı:")
    for m in get_last_matches("Real Madrid", "home"):
        print(f"{m['homeTeam']} {m['homeGoals']} - {m['awayGoals']} {m['awayTeam']}")
