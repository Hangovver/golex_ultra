import os
import requests
from datetime import datetime, timedelta

BASE_URL = "https://www.thesportsdb.com/api/v1/json"
API_KEY = os.getenv("TSD_API_KEY")  # Premium key (5-6 haneli sayı)

def _get(url, params=None):
    if not API_KEY:
        raise ValueError("TSD_API_KEY bulunamadı (Render Environment'a ekle).")
    full_url = f"{BASE_URL}/{API_KEY}/{url}"
    r = requests.get(full_url, params=params or {}, timeout=20)
    r.raise_for_status()
    return r.json()

def get_today_events():
    """Bugünkü (veya gerekirse dünkü) tüm futbol maçlarını döndürür."""
    today = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y-%m-%d")
    data = _get("eventsday.php", {"d": today, "s": "Soccer"})
    events = data.get("events") or []
    if not events:  # bazen gün farkı olabiliyor
        yest = (datetime.utcnow() + timedelta(hours=3) - timedelta(days=1)).strftime("%Y-%m-%d")
        data = _get("eventsday.php", {"d": yest, "s": "Soccer"})
        events = data.get("events") or []
    return events

def get_last_5_matches(team_id):
    """Bir takımın son 5 maçını döndürür."""
    data = _get("eventslast.php", {"id": team_id})
    return data.get("results") or []

def get_team_id_by_name(team_name):
    """Takım ismine göre TheSportsDB id'sini getirir."""
    data = _get("searchteams.php", {"t": team_name})
    teams = data.get("teams")
    if not teams:
        return None
    return teams[0].get("idTeam")
