# tools/analyzer.py
import requests
import statistics
from config import BASE_URL
import time

# Ana analiz fonksiyonu
def analyze_team_stats(team_id, mode="home_1.5"):
    try:
        url = f"{BASE_URL}/eventslast.php?id={team_id}"
        r = requests.get(url, timeout=10)
        data = r.json().get("results", [])
        if not data:
            return False

        # Son 5 maç
        recent = data[:5]

        # Gol istatistikleri
        goals_scored = [int(m.get("intHomeScore") or 0) if m["idHomeTeam"] == team_id
                        else int(m.get("intAwayScore") or 0) for m in recent]

        goals_conceded = [int(m.get("intAwayScore") or 0) if m["idHomeTeam"] == team_id
                          else int(m.get("intHomeScore") or 0) for m in recent]

        avg_scored = statistics.mean(goals_scored)
        avg_conceded = statistics.mean(goals_conceded)

        # --- Tahmin kriterleri ---
        if mode == "home_1.5":
            return all(g >= 2 for g in goals_scored)
        elif mode == "away_1.5":
            return all(g >= 2 for g in goals_scored)
        elif mode == "btts":
            return all((a > 0 and b > 0) for a, b in zip(goals_scored, goals_conceded))
        elif mode == "over_2.5":
            return all((a + b) >= 3 for a, b in zip(goals_scored, goals_conceded))
        elif mode == "btts_2.5":
            return all((a > 0 and b > 0 and (a + b) >= 3) for a, b in zip(goals_scored, goals_conceded))
        return False

    except Exception as e:
        print(f"⚠️ Analiz hatası: {e}")
        time.sleep(1)
        return False
