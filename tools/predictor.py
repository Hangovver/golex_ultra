# tools/predictor.py
from tools.alt_apifootball import get_last_matches_for_team

CONFIDENCE_THRESHOLD = 0.7  # %70 güven eşiği

def analyze_team_form(team_name, home_or_away):
    """Son 5 maçtan gol istatistiklerini ve başarı oranlarını hesapla."""
    matches = get_last_matches_for_team(team_name, home_or_away)
    if not matches:
        return {
            "ratios": {"ev_1_5": 0, "dep_1_5": 0, "kg": 0, "o2_5": 0, "kg_o2_5": 0},
            "samples": {"home_last5_home": 0, "away_last5_away": 0}
        }

    ev_1_5 = dep_1_5 = kg = o2_5 = kg_o2_5 = 0
    total_games = len(matches)

    for m in matches:
        home_goals = int(m["home_goals"])
        away_goals = int(m["away_goals"])
        total = home_goals + away_goals

        if home_goals >= 2:
            ev_1_5 += 1
        if away_goals >= 2:
            dep_1_5 += 1
        if home_goals > 0 and away_goals > 0:
            kg += 1
        if total >= 3:
            o2_5 += 1
        if total >= 3 and home_goals > 0 and away_goals > 0:
            kg_o2_5 += 1

    ratios = {
        "ev_1_5": round(ev_1_5 / total_games, 2),
        "dep_1_5": round(dep_1_5 / total_games, 2),
        "kg": round(kg / total_games, 2),
        "o2_5": round(o2_5 / total_games, 2),
        "kg_o2_5": round(kg_o2_5 / total_games, 2),
    }

    return {
        "ratios": ratios,
        "samples": {
            "home_last5_home": len(matches) if home_or_away == "home" else 0,
            "away_last5_away": len(matches) if home_or_away == "away" else 0
        }
    }


def best_pick_for_match(home_team, away_team):
    """Maç bazında en güçlü tahmini seç (tek seçenek, %70+ güvenle)."""
    home_stats = analyze_team_form(home_team, "home")
    away_stats = analyze_team_form(away_team, "away")

    # Ev & Dep istatistikleri birleştir
    combined_ratios = {
        "ev_1_5": home_stats["ratios"]["ev_1_5"],
        "dep_1_5": away_stats["ratios"]["dep_1_5"],
        "kg": max(home_stats["ratios"]["kg"], away_stats["ratios"]["kg"]),
        "o2_5": max(home_stats["ratios"]["o2_5"], away_stats["ratios"]["o2_5"]),
        "kg_o2_5": max(home_stats["ratios"]["kg_o2_5"], away_stats["ratios"]["kg_o2_5"]),
    }

    # Öncelik sırası
    priorities = ["kg_o2_5", "ev_1_5", "dep_1_5", "o2_5", "kg"]

    best_pick = None
    best_ratio = 0
    for key in priorities:
        ratio = combined_ratios[key]
        if ratio >= CONFIDENCE_THRESHOLD and ratio > best_ratio:
            best_pick = key
            best_ratio = ratio

    # Eğer hiçbir tahmin %70’in altında kalıyorsa, maç listelenmez
    if not best_pick:
        return None, None

    pick_labels = {
        "kg_o2_5": "KG + 2.5 ÜST",
        "ev_1_5": "Ev 1.5 ÜST",
        "dep_1_5": "Dep 1.5 ÜST",
        "o2_5": "2.5 ÜST",
        "kg": "KG (Karşılıklı Gol)"
    }

    pick_name = pick_labels[best_pick]
    confidence = int(best_ratio * 100)

    result = {
        "home": home_team,
        "away": away_team,
        "pick": pick_name,
        "confidence": confidence,
        "samples": {
            "home_last5_home": home_stats["samples"]["home_last5_home"],
            "away_last5_away": away_stats["samples"]["away_last5_away"]
        },
        "ratios": combined_ratios
    }

    return pick_name, result
