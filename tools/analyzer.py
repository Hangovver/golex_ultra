# analyzer.py
import requests
from config import BASE_URL
from statistics import mean

# Takımın son maçlarını al
def get_last_matches(team_id, count=5):
    url = f"{BASE_URL}/eventslast.php?id={team_id}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json().get("results", [])
        return data[:count] if data else []
    except Exception:
        return []

# Belirli tahmin türleri için oran hesaplama (yeni sürüm)
def analyze_team_stats(team_id, mode):
    matches = get_last_matches(team_id)
    if not matches or len(matches) < 3:
        return False  # Yetersiz veri

    goals_scored = []
    goals_conceded = []

    for m in matches:
        if not m.get("intHomeScore") or not m.get("intAwayScore"):
            continue
        if m["idHomeTeam"] == team_id:
            goals_scored.append(int(m["intHomeScore"]))
            goals_conceded.append(int(m["intAwayScore"]))
        else:
            goals_scored.append(int(m["intAwayScore"]))
            goals_conceded.append(int(m["intHomeScore"]))

    # En az 3 maç veri varsa analiz yap
    if len(goals_scored) < 3:
        return False

    # Ortalama hesaplama
    avg_scored = mean(goals_scored)
    avg_total = mean([sum(x) for x in zip(goals_scored, goals_conceded)])

    # 5 maçtan en az 3'ünde koşul sağlanıyorsa True
    cond = lambda cond_list: sum(cond_list) >= 3

    if mode == "home_1.5":
        return cond([g >= 2 for g in goals_scored])
    elif mode == "away_1.5":
        return cond([g >= 2 for g in goals_scored])
    elif mode == "btts":
        return cond([a > 0 and b > 0 for a, b in zip(goals_scored, goals_conceded)])
    elif mode == "over_2.5":
        return cond([(a + b) > 2 for a, b in zip(goals_scored, goals_conceded)])
    elif mode == "btts_2.5":
        return cond([(a > 0 and b > 0 and (a + b) > 2) for a, b in zip(goals_scored, goals_conceded)])
    else:
        return False
