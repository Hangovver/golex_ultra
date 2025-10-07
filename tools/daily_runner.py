# daily_runner.py
import requests
from datetime import datetime
from tools.predictor import analyze_match_strict

# ================== AYARLAR ==================
SPORT_API_KEY = "YOUR_SPORTAPI_KEY"  # api-sports.io veya sportdataapi key
SPORT_API_HOST = "v3.football.api-sports.io"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
# ============================================


def send_telegram(msg: str):
    """Telegram’a mesaj gönderir"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    r = requests.post(url, json=payload)
    print("Telegram yanıtı:", r.text)
    return r


def get_today_matches():
    """Sport API'den bugünün maçlarını alır"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = f"https://{SPORT_API_HOST}/fixtures?date={today}"
    headers = {"x-apisports-key": SPORT_API_KEY}
    r = requests.get(url, headers=headers)
    data = r.json()
    if "response" not in data or not data["response"]:
        return []
    return data["response"]


def get_last5_matches(team_id: int, home: bool):
    """Belirtilen takımın son 5 ev/deplasman maçını getirir"""
    url = f"https://{SPORT_API_HOST}/fixtures?team={team_id}&last=10"
    headers = {"x-apisports-key": SPORT_API_KEY}
    r = requests.get(url, headers=headers)
    data = r.json()
    if "response" not in data:
        return []

    matches = []
    for m in data["response"]:
        if home and m["teams"]["home"]["id"] == team_id:
            matches.append({
                "home_goals": m["goals"]["home"],
                "away_goals": m["goals"]["away"],
            })
        elif not home and m["teams"]["away"]["id"] == team_id:
            matches.append({
                "home_goals": m["goals"]["home"],
                "away_goals": m["goals"]["away"],
            })
    return matches[:5]


def get_injuries(team_id: int):
    """Takımın as oyuncu sakatlıklarını getirir"""
    url = f"https://{SPORT_API_HOST}/injuries?team={team_id}"
    headers = {"x-apisports-key": SPORT_API_KEY}
    r = requests.get(url, headers=headers)
    data = r.json()
    injuries = []
    if "response" in data:
        for p in data["response"]:
            if p["player"]["name"] and p["player"]["type"] in ["Injury", "Suspended"]:
                injuries.append(p["player"]["name"])
    return injuries


def run_daily_analysis():
    matches = get_today_matches()
    if not matches:
        send_telegram("⚽️ Bugün maç bulunamadı 😅")
        print("Bugün maç bulunamadı.")
        return

    results = []
    for m in matches:
        home_team = m["teams"]["home"]["name"]
        away_team = m["teams"]["away"]["name"]
        id_home = m["teams"]["home"]["id"]
        id_away = m["teams"]["away"]["id"]

        # Maç verilerini çek
        home_last5 = get_last5_matches(id_home, home=True)
        away_last5 = get_last5_matches(id_away, home=False)

        # Sakat oyuncuları çek
        home_injuries = get_injuries(id_home)
        away_injuries = get_injuries(id_away)

        preds = analyze_match_strict(home_last5, away_last5, home_injuries, away_injuries)

        if preds and "analiz dışı" not in preds[0]:
            results.append(f"{home_team} - {away_team} → {', '.join(preds)}")
        elif preds and "analiz dışı" in preds[0]:
            results.append(f"{home_team} - {away_team} ⚠️ As oyuncu sakatlığı nedeniyle analiz dışı")
        else:
            results.append(f"{home_team} - {away_team} → (kriterleri sağlamıyor)")

    if not results:
        send_telegram("📊 Bugün kriterlere uygun maç bulunamadı.")
        print("Hiç uygun maç bulunamadı.")
        return

    msg = "📊 GOLEX Günlük Analiz\n\n" + "\n".join(results)
    send_telegram(msg)
    print(msg)


if __name__ == "__main__":
    run_daily_analysis()
