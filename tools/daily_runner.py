from tools.alt_thesportsdb import get_today_events, get_team_id_by_name, get_last5_by_team
import requests

# 🔧 Telegram bilgilerini buraya ekle
TELEGRAM_TOKEN = "8227478980:AAGF1g0PHGp6j85SG8qPyyP9hYjgfJcWyRU"
CHAT_ID = "5876994093"

def analyze_team(team_name: str):
    team_id = get_team_id_by_name(team_name)
    if not team_id:
        return {"team": team_name, "avg_goals": 0.0}

    matches = get_last5_by_team(team_id)
    if not matches:
        return {"team": team_name, "avg_goals": 0.0}

    total_goals = 0
    for m in matches:
        if m.get("intHomeScore") and m.get("intAwayScore"):
            total_goals += int(m["intHomeScore"]) + int(m["intAwayScore"])
    avg_goals = total_goals / len(matches)
    return {"team": team_name, "avg_goals": round(avg_goals, 2)}

def analyze_match(home, away):
    h = analyze_team(home)
    a = analyze_team(away)
    avg_total = round((h["avg_goals"] + a["avg_goals"]) / 2, 2)
    return f"{home} vs {away} ⚽ Ortalama {avg_total} gol beklentisi."

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

def run_and_notify():
    print("⚡ Günlük analiz başlatıldı...")
    events = get_today_events()
    if not events:
        send_telegram_message("Bugün maç bulunamadı ⚽")
        return

    messages = []
    for e in events:
        home = e.get("strHomeTeam")
        away = e.get("strAwayTeam")
        if not home or not away:
            continue
        result = analyze_match(home, away)
        messages.append(result)

    final_msg = "\n".join(messages)
    send_telegram_message(f"📅 Günlük Analiz:\n\n{final_msg}")
    print("✅ Analiz tamamlandı ve Telegram’a gönderildi.")
