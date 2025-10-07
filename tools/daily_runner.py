from tools.alt_thesportsdb import get_last_5_matches, get_team_id_by_name

def analyze_team(team_name):
    """Bir takımın son 5 maçına göre gol analizleri"""
    team_id = get_team_id_by_name(team_name)
    if not team_id:
        return None

    matches = get_last_5_matches(team_id)
    if not matches:
        return None

    home_goals = []
    away_goals = []
    total_goals = []
    both_scored = []

    for m in matches:
        try:
            h = int(m.get("intHomeScore", 0) or 0)
            a = int(m.get("intAwayScore", 0) or 0)
            home = m.get("strHomeTeam")
            away = m.get("strAwayTeam")

            total_goals.append(h + a)
            both_scored.append(h > 0 and a > 0)

            if team_name.lower() in home.lower():
                home_goals.append(h)
            elif team_name.lower() in away.lower():
                away_goals.append(a)
        except:
            continue

    avg_home = sum(home_goals) / len(home_goals) if home_goals else 0
    avg_away = sum(away_goals) / len(away_goals) if away_goals else 0
    avg_total = sum(total_goals) / len(total_goals) if total_goals else 0
    kg_rate = both_scored.count(True) / len(both_scored) if both_scored else 0

    return {
        "team": team_name,
        "ev_15_plus": avg_home >= 1.5,
        "dep_15_plus": avg_away >= 1.5,
        "ust_25": avg_total >= 2.5,
        "kg": kg_rate >= 0.6,
        "kg_ust_25": (kg_rate >= 0.6 and avg_total >= 2.5)
    }

def analyze_match(home_team, away_team):
    """İki takımı karşılaştırır ve olası tahminleri döner"""
    home = analyze_team(home_team)
    away = analyze_team(away_team)

    if not home or not away:
        return None

    result = {
        "match": f"{home_team} vs {away_team}",
        "ev_15_plus": home["ev_15_plus"],
        "dep_15_plus": away["dep_15_plus"],
        "ust_25": home["ust_25"] or away["ust_25"],
        "kg": home["kg"] and away["kg"],
        "kg_ust_25": home["kg_ust_25"] and away["kg_ust_25"]
    }

    return result

if __name__ == "__main__":
    matches = [
        ("Manchester United", "Chelsea"),
        ("Fenerbahce", "Galatasaray"),
        ("Barcelona", "Real Madrid")
    ]

    for home, away in matches:
        result = analyze_match(home, away)
        if result:
            print(result)
