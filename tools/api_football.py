import os
import requests
from datetime import datetime

def get_today_matches():
    """
    Football-Data.org API'sinden bugünkü maçları çeker.
    """
    try:
        api_key = os.getenv("FOOTBALL_DATA_KEY")
        if not api_key:
            return ["API anahtarı bulunamadı. Lütfen FOOTBALL_DATA_KEY ortam değişkenini ekle."]

        headers = {"X-Auth-Token": api_key}
        today = datetime.utcnow().strftime("%Y-%m-%d")
        url = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={today}"

        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return [f"API hatası ({response.status_code}): {response.text}"]

        data = response.json()
        matches = []

        for match in data.get("matches", []):
            home = match.get("homeTeam", {}).get("name", "Bilinmiyor")
            away = match.get("awayTeam", {}).get("name", "Bilinmiyor")
            competition = match.get("competition", {}).get("name", "")
            status = match.get("status", "")
            utc_date = match.get("utcDate", "")

            match_str = f"{home} vs {away} ({competition}) [{status}]"
            if utc_date:
                match_str += f" - {utc_date[:16].replace('T', ' ')}"
            matches.append(match_str)

        if not matches:
            return ["Bugün için maç bulunamadı."]

        return matches

    except Exception as e:
        return [f"⚠️ API hatası: {e}"]
