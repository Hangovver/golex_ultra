# tools/analyzer.py
import time
import requests
from typing import List, Dict
from config import BASE_URL

# Küçük yardımcılar
def _to_int(x):
    try:
        return int(x)
    except Exception:
        return None

def _get(path: str, params: Dict = None, timeout=12) -> dict:
    url = f"{BASE_URL}/{path}"
    r = requests.get(url, params=params or {}, timeout=timeout)
    r.raise_for_status()
    return r.json() or {}

def fetch_last_events(team_id: str) -> List[dict]:
    """
    TheSportsDB: eventslast.php?id=TEAM
    Son 5 maçı döner (home+away karışık).
    """
    data = _get("eventslast.php", {"id": team_id})
    events = data.get("results") or data.get("events") or []
    return events

def last5_home(team_id: str) -> List[dict]:
    # eventslast sadece 5 maç döndürdüğü için bazen 5 home/away çıkmayabilir.
    # Bu durumda "yeterli veri yok" sayıp False döneceğiz.
    events = fetch_last_events(team_id)
    home = [e for e in events if e.get("idHomeTeam") == team_id][:5]
    return home

def last5_away(team_id: str) -> List[dict]:
    events = fetch_last_events(team_id)
    away = [e for e in events if e.get("idAwayTeam") == team_id][:5]
    return away

# ---- Kriterler (hepsi "SON 5" için "her maç" şartı) ----

def meets_home_1_5(team_id: str) -> bool:
    """
    Ev 1.5 Üst: ev sahibinin evindeki son 5 maçın HER BİRİNDE en az 2 gol atması.
    """
    games = last5_home(team_id)
    if len(games) < 5:
        return False
    for g in games:
        gh = _to_int(g.get("intHomeScore"))
        if gh is None or gh < 2:
            return False
    return True

def meets_away_1_5(team_id: str) -> bool:
    """
    Dep 1.5 Üst: deplasmanın deplasmandaki son 5 maçın HER BİRİNDE en az 2 gol atması.
    """
    games = last5_away(team_id)
    if len(games) < 5:
        return False
    for g in games:
        ga = _to_int(g.get("intAwayScore"))
        if ga is None or ga < 2:
            return False
    return True

def meets_btts_pair(home_id: str, away_id: str) -> bool:
    """
    KG Var: evin EVDE son 5 maçının her birinde en az 1 gol atmış olması
            ve deplesmanın DEPLASMANDA son 5 maçının her birinde en az 1 gol atmış olması.
    """
    h = last5_home(home_id)
    a = last5_away(away_id)
    if len(h) < 5 or len(a) < 5:
        return False
    for g in h:
        gh = _to_int(g.get("intHomeScore"))
        if gh is None or gh < 1:
            return False
    for g in a:
        ga = _to_int(g.get("intAwayScore"))
        if ga is None or ga < 1:
            return False
    return True

def meets_over25_pair(home_id: str, away_id: str) -> bool:
    """
    2.5 Üst: evin EVDE son 5 maçının her birinde toplam gol >=3
             ve deplasmanın DEPLASMANDA son 5 maçının her birinde toplam gol >=3
    """
    h = last5_home(home_id)
    a = last5_away(away_id)
    if len(h) < 5 or len(a) < 5:
        return False
    for g in h:
        gh = _to_int(g.get("intHomeScore")); ga = _to_int(g.get("intAwayScore"))
        if gh is None or ga is None or (gh + ga) < 3:
            return False
    for g in a:
        gh = _to_int(g.get("intHomeScore")); ga = _to_int(g.get("intAwayScore"))
        if gh is None or ga is None or (gh + ga) < 3:
            return False
    return True

def meets_btts_over25_pair(home_id: str, away_id: str) -> bool:
    """
    KG + 2.5: hem KG kriteri hem de 2.5 Üst kriteri (ikisi de her maç için) sağlanmalı.
    """
    return meets_btts_pair(home_id, away_id) and meets_over25_pair(home_id, away_id)
