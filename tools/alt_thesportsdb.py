import os
import requests

API_KEY = os.getenv("THESPORTSDB_KEY")

BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

def get_last_5_matches(team_id: str):
    """Takımın son 5 maçını döndürür"""
    url = f"{BASE_URL}/eventslast.php?id={team_id}"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        return data.get("results", [])[:5]
    except Exception as e:
        print(f"[ERROR] get_last_5_matches failed for team {team_id}: {e}")
        return []

def get_team_id_by_name(team_name: str, sport: str = "Soccer"):
    """Takım ismine göre team_id getirir"""
    url = f"{BASE_URL}/searchteams.php?t={team_name}"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        if data and data.get("teams"):
            return data["teams"][0]["idTeam"]
    except Exception as e:
        print(f"[ERROR] get_team_id_by_name failed for {team_name}: {e}")
    return None
