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
        today = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y-%m-%d")  # Türkiye saati
        url = f"{BASE_URL}/fixtures?date={today}"
        headers = {"x-apisports-key": API_KEY}

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

        return matches[:30]

    except Exception as e:
        print(f"❌ Maç verisi alınamadı: {e}")
        return []


def get_team_goal_average(team_name):
    """
    Belirli bir takımın son 5 maçtaki gol ortalamasını döndürür.
    """
    try:
        headers = {"x-apisports-key": API_KEY}

        team_search_url = f"{BASE_URL}/teams?search={team_name}"
        team_res = requests.get(team_search_url, headers=headers, timeout=10).json()
        if not team_res.get("response"):
            return 0

        team_id = team_res["response"][0]["team"]["id"]

        fixtures_url = f"{BASE_URL}/fixtures?team={team_id}&last=5"
        fixtures_res = requests.get(fixtures_url, headers=headers, timeout=10).json()
        fixtures = fixtures_res.get("response", [])

        goals = 0
        match_count = 0
        for fx in fixtures:
            try:
                g = fx["teams"]["home"]["goals"]["for"] if fx["teams"]["home"]["name"] == team_name else fx["teams"]["away"]["goals"]["for"]
                goals += g
                match_count += 1
            except:
                continue

        return round(goals / match_count, 2) if match_count else 0

    except Exception as e:
        print(f"⚠️ Takım istatistiği alınamadı ({team_name}): {e}")
        return 0
