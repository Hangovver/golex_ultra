# -*- coding: utf-8 -*-
from __future__ import annotations
import os
from datetime import datetime, timezone
from typing import List

import requests

# TELEGRAM göndericiyi projendeki adıyla bırakıyorum
# (sende tools/telegram.py var diye varsayıyorum)
from .telegram import send_telegram_message  # noqa: F401

# Mevcut API-FOOTBALL çekicin varsa kalsın; yoksa try/except ile atlarız
def _get_from_api_football(limit: int = 30) -> List[str]:
    api_key = os.getenv("API_FOOTBALL_KEY") or os.getenv("X_RAPIDAPI_KEY")
    if not api_key:
        return []
    try:
        # RapidAPI host/endpoint (v3). Varsa kendi fonksiyonunu da çağırabilirsin.
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        params = {"date": today, "timezone": "UTC"}
        headers = {
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
            "x-rapidapi-key": api_key,
        }
        r = requests.get(url, params=params, headers=headers, timeout=25)
        if r.status_code != 200:
            return []
        j = r.json() or {}
        res = j.get("response") or []
        out: List[str] = []
        for it in res:
            teams = it.get("teams") or {}
            home = ((teams.get("home") or {}).get("name") or "").strip()
            away = ((teams.get("away") or {}).get("name") or "").strip()
            league = ((it.get("league") or {}).get("name") or "").strip()
            time_utc = ((it.get("fixture") or {}).get("date") or "").strip()
            label = f"{home} – {away}".strip(" –")
            extra = f"({league})" if league else ""
            piece = " ".join(x for x in [label, extra] if x).strip()
            if time_utc:
                piece += f" {time_utc}"
            if label:
                out.append(piece)
        return out[:limit]
    except Exception:
        return []

# Football-Data.org (token varsa) – ücretsiz ve hızlı
def _get_from_footballdata(limit: int = 30) -> List[str]:
    token = os.getenv("FOOTBALL_DATA_TOKEN")
    if not token:
        return []
    try:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        url = f"https://api.football-data.org/v4/matches"
        params = {"dateFrom": today, "dateTo": today}
        headers = {"X-Auth-Token": token}
        r = requests.get(url, params=params, headers=headers, timeout=20)
        if r.status_code != 200:
            return []
        j = r.json() or {}
        matches = j.get("matches") or []
        out: List[str] = []
        for m in matches:
            comp = ((m.get("competition") or {}).get("name") or "").strip()
            home = ((m.get("homeTeam") or {}).get("name") or "").strip()
            away = ((m.get("awayTeam") or {}).get("name") or "").strip()
            label = f"{home} – {away}".strip(" –")
            extra = f"({comp})" if comp else ""
            piece = " ".join(x for x in [label, extra] if x).strip()
            if label:
                out.append(piece)
        return out[:limit]
    except Exception:
        return []

# TheSportsDB (public) – anahtarsız fallback
from .alt_thesportsdb import get_today_matches_thesportsdb  # noqa: E402

def run_daily_analysis(max_matches: int = 30) -> str:
    # Başlık
    today_human = datetime.now(timezone.utc).strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today_human})\n\n"
    message += "⚽️ Bugünkü Maçlar:\n"

    # 1) API-FOOTBALL (varsa)  2) Football-Data (varsa)  3) TheSportsDB (public)
    matches: List[str] = []
    for getter in (_get_from_api_football, _get_from_footballdata, get_today_matches_thesportsdb):
        try:
            matches = getter(max_matches)
            if matches:
                break
        except Exception:
            continue

    if not matches:
        message += "Bugün maç bulunamadı 😅\n"
    else:
        # UTF-8 güvenli liste
        for m in matches[:max_matches]:
            safe = str(m).encode("utf-8", errors="ignore").decode("utf-8").strip()
            if safe:
                message += f"• {safe}\n"

    message += "🔮 Tahminler istatistiklere göre sıralanacak."
    # Telegram’a gönder
    try:
        send_telegram_message(message)
    except Exception:
        pass
    return message

