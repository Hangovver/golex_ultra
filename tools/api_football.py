import requests
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://v3.football.api-sports.io"

def get_today_matches():
    """
    Bugünün maçlarını çeker ve istatistiklere göre tahminler üretir.
    """
    try:
        # Türkiye saatine göre tarih (Render UTC çalışıyor)
        today = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y-%m-%d")
        url = f"{BASE_URL}/fixtures?date={today}"

        headers = {
            "x-apisports-key": API_KEY
        }

        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()

        if not data.get("response"):
            print(f"⚠️ API boş döndü! Tarih: {today}")
            return []

        matches = []
        for item in data["response"]:
            try:
                home = item["teams"]["home"]["name"]
                away = item["teams"]["away"]["name"]
                fixture_id = item["fixture"]["id"]

                # Her takımın son 5 maç istatistiklerini alalım
                home_avg = get_team_goal_average(home)
                away_avg = get_team_goal_average(away)

                # Tahmin kuralları
                if home_avg > 2 and away_avg > 2:
                    prediction = "2.5 ÜST ⚡"
                elif home_avg > 1.5 and away_avg > 1:
                    prediction = "KG VAR 🔥"
                elif home_avg > 1.5:
                    prediction = "Ev 1.5+ ⚽"
                elif away_avg > 1.5:
                    prediction = "Dep 1.5+ ⚽"
                else:
                    prediction = "1.5 ÜST ⚙️"

                matches.append(f"{home} vs {away} → {prediction}")

            except Exception as inner_e:
                print(f"⚠️ Maç işlenemedi: {inner_e}")
                continue

        return matches[:30]  # Maksimum 30 maç

    except Exception as e:
        print(f"❌ Maç verisi alınamadı: {e}")
        return []

def get_team_goal_average(team_name):
    """
    Belirli bir takımın son 5 maçtaki gol ortalamasını döndürür.
    """
    try:
        url = f"{BASE_URL}/teams?search={team_name}"
        headers = {"x-apisports-key": API_KEY}
        res = requests.get(url, headers=headers, timeout=10)
        team_data = res.json()

        if not team_data["response"]:
            return 0

        team_id = team_data["response"][0]["team"]["id"]

        # Son 5 maç
        url_fixtures = f"{BASE_URL}/fixtures?team={team_id}&last=5"
        res_fixtures = requests.get(url_fixtures, headers=headers, timeout=10)
        fixtures = res_fixtures.json().get("response", [])

        goals = 0
        match_count = 0

        for fx in fixtures:
            goals += fx["goals"]["for"]["total"]["total"] if "for" in fx["goals"] else 0
            match_count += 1

        return round(goals / match_count, 2) if match_count > 0 else 0

    except Exception as e:
        print(f"⚠️ Takım istatistiği alınamadı ({team_name}): {e}")
        return 0
