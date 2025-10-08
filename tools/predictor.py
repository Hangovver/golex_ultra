# tools/predictor.py
from tools.alt_apifootball import get_last_matches

def _over_15_goals(matches, team_name, side):
    """Belirtilen tarafın maçlarında 2+ gol atıp atmadığı (1.5 üst)"""
    count = 0
    for m in matches:
        if side == "home":
            if m["homeTeam"] == team_name and m["homeGoals"] >= 2:
                count += 1
        else:
            if m["awayTeam"] == team_name and m["awayGoals"] >= 2:
                count += 1
    return count >= 3  # 5 maçtan 3'ünde 2+ gol

def _btts(matches):
    """Her iki takım da gol atmış mı (Both Teams To Score)"""
    return sum(1 for m in matches if m["homeGoals"] > 0 and m["awayGoals"] > 0) >= 3

def _over25(matches):
    """Maç 2.5 üst olmuş mu"""
    return sum(1 for m in matches if m["homeGoals"] + m["awayGoals"] >= 3) >= 3

def best_pick_for_match(home_team, away_team):
    """Ana tahmin motoru"""
    try:
        home_last = get_last_matches(home_team, "home")
        away_last = get_last_matches(away_team, "away")
    except Exception as e:
        return {"error": str(e)}, {}

    # Kriterler
    ev15 = _over_15_goals(home_last, home_team, "home")
    dep15 = _over_15_goals(away_last, away_team, "away")

    # Kombine 10 maçta analiz
    combined = home_last + away_last
    kg = _btts(combined)
    over25 = _over25(combined)
    kg_over25 = kg and over25

    pick = None
    if ev15:
        pick = "🏠 Ev 1.5 ÜST"
    elif dep15:
        pick = "🚗 Dep 1.5 ÜST"
    elif kg_over25:
        pick = "💥 KG + 2.5"
    elif kg:
        pick = "⚽ KG VAR"
    elif over25:
        pick = "🔥 2.5 ÜST"

    info = {
        "criteria": {
            "ev1.5": ev15,
            "dep1.5": dep15,
            "kg": kg,
            "2.5": over25,
            "kg+2.5": kg_over25,
        },
        "samples": {"Ev": len(home_last), "Dep": len(away_last)},
    }

    return (pick or "⚪ Uygun tahmin yok"), info
