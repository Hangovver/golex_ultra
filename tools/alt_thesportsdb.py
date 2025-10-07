import requests
import time
from datetime import date

API_KEY = "099583"  # Örn: "099583"
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

def _get(endpoint, params=None):
    """Genel GET isteği (otomatik tekrar ve limit koruması içerir)"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        r = requests.get(url, params=params)
        if r.status_code == 429:
            print("⚠️ Too many requests (429) — 3 saniye bekleniyor...")
            time.sleep(3)
            return _get(endpoint, params)
        r.raise_for_status()
        time.sleep(0.5)  # API limitini aşmamak için ufak gecikme
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"🚨 API hatası: {e}")
        return None

def get_today_events():
    """Bugünkü futbol maçlarını döndürür"""
    today = date.today().isoformat()
    data = _get("eventsday.php", {"d": today, "s": "Soccer"})
    if not data or not data.get("events"):
        print("⚽ Bugün için etkinlik bulunamadı.")
        return []
    return data["events"]

def get_team_id_by_name(team_name: str):
    """Takım ismine göre ID döndürür"""
    data = _get("searchteams.php", {"t": team_name})
    if data and data.get("teams"):
        return data["teams"][0]["idTeam"]
    print(f"Takım bulunamadı: {team_name}")
    return None

def get_last5_by_team(team_id: str):
    """Takımın son 5 maçını döndürür"""
    data = _get("eventslast.php", {"id": team_id})
    if data and data.get("results"):
        return data["results"][:5]
    return []
