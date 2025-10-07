# tools/alt_thesportsdb.py
import requests
import time
from config import API_KEY, BASE_URL

# API istek sınırı kontrolü (rate limit)
MAX_RETRIES = 3
SLEEP_TIME = 10  # saniye

def _get(endpoint, params=None):
    """TheSportsDB API isteği, limit kontrolü ile"""
    url = f"{BASE_URL}/{endpoint}"
    headers = {"User-Agent": "Golex-Ultra/1.0"}
    for attempt in range(1, MAX_RETRIES + 1):
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 429:
            print(f"⚠️ Too many requests — {SLEEP_TIME} saniye bekleniyor... (Deneme {attempt}/{MAX_RETRIES})")
            time.sleep(SLEEP_TIME)
        else:
            print(f"❌ API hatası: {r.status_code} - {r.text}")
            break
    return None


def get_team_id_by_name(team_name: str):
    """Takım adından ID bulur"""
    data = _get("searchteams.php", {"t": team_name})
    if not data or not data.get("teams"):
        print(f"⚠️ Takım bulunamadı: {team_name}")
        return None
    return data["teams"][0]["idTeam"]


def get_last_5_matches(team_id: str):
    """Takımın son 5 maçını çeker"""
    data = _get("eventslast.php", {"id": team_id})
    if not data or not data.get("results"):
        return []
    return data["results"][:5]


def get_today_events():
    """Bugünün maçlarını çeker"""
    data = _get("eventsday.php", {"d": time.strftime("%Y-%m-%d")})
    if not data or not data.get("events"):
        print("⚠️ Bugün için maç bulunamadı.")
        return []
    return data["events"]
