# tools/alt_apifootball.py
import requests
from datetime import datetime
from functools import lru_cache
from config import BASE_URL_FOOTBALL, API_FOOTBALL_KEY

HEADERS = {"x-apisports-key": API_FOOTBALL_KEY}


def _get(endpoint: str, params: dict = None):
    url = f"{BASE_URL_FOOTBALL}/{endpoint}"
    r = requests.get(url, params=params or {}, headers=HEADERS, timeout=20)
    if r.status_code != 200:
        raise RuntimeError(f"API error {r.status_code}: {r.text[:200]}")
    return r.json().get("response", [])


def get_today_events(limit=None):
    """Bugünkü maçları (fixture) getirir"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    data = _get("fixtures", {"date": today})
    if limit:
        data = data[:limit]
    return data


@lru_cache(maxsize=512)
def get_last_events(team_id: int, limit=5):
    """Bir takımın son maçlarını getirir"""
    data = _get("fixtures", {"team": team_id, "last": limit})
    return data


def goals(evt: dict):
    """Maç skorunu (ev, dep) döndürür"""
    try:
        goals = evt.get("goals") or {}
        return goals.get("home"), goals.get("away")
    except Exception:
        return None


def team_id_from_event(evt: dict):
    """Fixture içinden ev ve deplasman ID’lerini döndürür"""
    try:
        home = evt["teams"]["home"]
        away = evt["teams"]["away"]
        return home.get("id"), away.get("id")
    except Exception:
        return None, None
