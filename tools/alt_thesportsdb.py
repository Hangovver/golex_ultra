# tools/alt_thesportsdb.py
import time
import requests
from functools import lru_cache
from datetime import datetime
from config import BASE_URL

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Golex/1.0"})

def _get(path: str, params: dict, retry=True):
    url = f"{BASE_URL}/{path}"
    r = SESSION.get(url, params=params, timeout=20)
    if r.status_code == 429:
        if retry:
            print("⚠️ Too many requests — 10 saniye bekleniyor...")
            time.sleep(10)
            return _get(path, params, retry=False)
    r.raise_for_status()
    return r.json() if r.text else {}

def today_ymd():
    # TheSportsDB 'eventsday' UTC kabul ediyor. Gerekirse +03 offseti burada verilir.
    return datetime.utcnow().strftime("%Y-%m-%d")

@lru_cache(maxsize=512)
def get_team_id_by_name(team_name: str) -> str | None:
    data = _get("searchteams.php", {"t": team_name})
    teams = (data or {}).get("teams") or []
    if not teams:
        return None
    return teams[0].get("idTeam")

def get_today_events(limit=None) -> list[dict]:
    data = _get("eventsday.php", {"d": today_ymd(), "s": "Soccer"})
    events = (data or {}).get("events") or []
    if limit is not None:
        events = events[:limit]
    return events

@lru_cache(maxsize=1024)
def get_last_events(team_id: str) -> list[dict]:
    # TheSportsDB: eventslast.php?id=TEAM_ID (genelde 5-10 maç döner)
    data = _get("eventslast.php", {"id": team_id})
    evts = (data or {}).get("results") or []
    # En yeni üste gelebilir; genele karışmasın diye tarih/ID’ye göre sıralıyoruz
    def keyf(e):
        # sırala: dateEvent + idEvent
        return ((e.get("dateEvent") or "1900-01-01"), str(e.get("idEvent") or "0"))
    return sorted(evts, key=keyf, reverse=True)

def is_home_event(evt: dict, team_name: str) -> bool:
    return (evt.get("strHomeTeam") or "").strip().lower() == team_name.strip().lower()

def is_away_event(evt: dict, team_name: str) -> bool:
    return (evt.get("strAwayTeam") or "").strip().lower() == team_name.strip().lower()

def goals(evt: dict) -> tuple[int,int] | None:
    try:
        hs = evt.get("intHomeScore")
        as_ = evt.get("intAwayScore")
        if hs is None or as_ is None:
            return None
        return int(hs), int(as_)
    except Exception:
        return None

def last5_home(team_name: str) -> list[dict]:
    tid = get_team_id_by_name(team_name)
    if not tid:
        return []
    evts = get_last_events(tid)
    only_home = [e for e in evts if is_home_event(e, team_name)]
    return only_home[:5]

def last5_away(team_name: str) -> list[dict]:
    tid = get_team_id_by_name(team_name)
    if not tid:
        return []
    evts = get_last_events(tid)
    only_away = [e for e in evts if is_away_event(e, team_name)]
    return only_away[:5]
