# tools/alt_apifootball.py
import os
import requests

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}


def get_team_id_by_name(team_name):
    """Takım adından ID bulur."""
    url = f"{BASE_URL}/teams"
    params = {"search": team_name}
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    data = r.json().get("response", [])
    if not data:
        return None
    return data[0]["team"]["id"]


def get_last_matches_for_team(team_name, home_or_away="home"):
    """
    Belirtilen takımın son 5 maçını döner.
    home_or_away: 'home' → iç saha maçları, 'away' → deplasman maçları
    """
    team_id = get_team_id_by_name(team_name)
    if not team_id:
        print(f"⚠️ Takım bulunamadı: {team_name}")
        return []

    url = f"{BASE_URL}/fixtures"
    params = {"team": team_id, "last": 10}  # 10 maçtan son 5'ini filtreleyeceğiz
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    data = r.json().get("response", [])
    if not data:
        return []

    matches = []
    for m in data:
        fixture = m.get("fixture", {})
        teams = m.get("teams", {})
        goals = m.get("goals", {})

        is_home = teams.get("home", {}).get("id") == team_id
        if home_or_away == "home" and not is_home:
            continue
        if home_or_away == "away" and is_home:
            continue

        matches.append({
            "home_team": teams.get("home", {}).get("name"),
            "away_team": teams.get("away", {}).get("name"),
            "home_goals": goals.get("home", 0) or 0,
            "away_goals": goals.get("away", 0) or 0,
        })

        if len(matches) >= 5:
            break  # sadece son 5 maç

    return matches


def get_today_events():
    """Bugünkü maçları döner (League / Country fark etmez)."""
    from datetime import date
    today = date.today().isoformat()

    url = f"{BASE_URL}/fixtures"
    params = {"date": today}
    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    data = r.json().get("response", [])
    if not data:
        return []

    matches = []
    for m in data:
        teams = m.get("teams", {})
        matches.append({
            "home": teams.get("home", {}).get("name"),
            "away": teams.get("away", {}).get("name"),
            "id": m.get("fixture", {}).get("id"),
        })
    return matches
