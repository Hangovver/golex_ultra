import requests
import datetime
import os

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}


def get_today_matches():
    """Bugünkü maçları ve tahminleri döndürür"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/fixtures?date={today}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"API hatası: {response.status_code}")

    data = response.json().get("response", [])
    matches = []

    for match in data[:30]:  # 🔹 30 maç sınırı
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        # 🔮 Tahmini hesapla
        prediction = generate_prediction(home_id, away_id)
        matches.append(f"{home} vs {away} → {prediction}")

    return matches


def generate_prediction(home_id, away_id):
    """Son 5 maça göre basit tahmin oluşturur"""
    try:
        home_form = get_team_form(home_id)
        away_form = get_team_form(away_id)

        if not home_form or not away_form:
            return "Veri eksik ⚠️"

        home_avg = sum(home_form) / len(home_form)
        away_avg = sum(away_form) / len(away_form)

        # 🔹 Ev / Deplasman 1.5 üst tahmini
        if home_avg >= 2 and away_avg < 1.5:
            return "Ev 1.5 Üst"
        elif away_avg >= 2 and home_avg < 1.5:
            return "Dep 1.5 Üst"

        # 🔹 Her iki takım da yüksek gol ortalamalıysa
        elif home_avg >= 1.5 and away_avg >= 1.5:
            return "KG Var & 2.5 Üst"

        else:
            return "Alt veya KG Yok"
    except Exception as e:
        return f"Hata: {e}"


def get_team_form(team_id):
    """Takımın son 5 maçtaki gol ortalamasını döndürür"""
    try:
        url = f"{BASE_URL}/fixtures?team={team_id}&last=5"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return []

        matches = response.json().get("response", [])
        goals = []

        for m in matches:
            team_home = m["teams"]["home"]["id"] == team_id
            if team_home:
                goals.append(m["goals"]["home"])
            else:
                goals.append(m["goals"]["away"])

        return goals
    except:
        return []
