# -*- coding: utf-8 -*-
"""
TheSportsDB (public) fallback.
Anahtar gerektirmez (test key = '1').
Bugünün 'Soccer' maçlarını döndürür.
"""
from __future__ import annotations
import os
import requests
from datetime import datetime, timezone
from typing import List

def get_today_matches_thesportsdb(limit: int = 30) -> List[str]:
    # Gün (UTC) — kaynak UTC döndüğü için sade tutuyoruz
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    api_key = os.getenv("THESPORTSDB_KEY", "1")  # test anahtarı
    url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventsday.php"
    params = {"d": today, "s": "Soccer"}

    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json() or {}
        events = data.get("events") or []
        matches: List[str] = []
        for e in events:
            # Güvenli alan okuma
            home = (e.get("strHomeTeam") or "").strip()
            away = (e.get("strAwayTeam") or "").strip()
            league = (e.get("strLeague") or "").strip()
            tlocal = (e.get("strTimeLocal") or e.get("strTime") or "").strip()
            if not home or not away:
                # strEvent "TeamA vs TeamB" formatında olabilir
                ev = (e.get("strEvent") or "").strip()
                if " vs " in ev:
                    home, away = [p.strip() for p in ev.split(" vs ", 1)]
            if home and away:
                label = f"{home} – {away}"
                ext = " ".join(x for x in [f"({league})" if league else "", tlocal] if x).strip()
                matches.append(f"{label} {ext}".strip())
        return matches[:limit]
    except Exception:
        return []
