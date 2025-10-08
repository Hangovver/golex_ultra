# tools/predictor.py
from tools.alt_apifootball import get_last_events, goals


def _all_matches_scored_at_least(evts, need, as_home):
    if len(evts) < 2:  # ⚠️ 5 yerine 2 yaptık çünkü API bazen eksik döner
        return False
    for e in evts:
        g = goals(e)
        if not g or g[0] is None or g[1] is None:
            continue
        team_goals = g[0] if as_home else g[1]
        if team_goals < need:
            return False
    return True


def _all_matches_over_total(evts, line):
    if len(evts) < 2:
        return False
    for e in evts:
        g = goals(e)
        if not g or g[0] is None or g[1] is None:
            continue
        if (g[0] + g[1]) < line:
            return False
    return True


def _all_matches_scored_at_least_one(evts, as_home):
    return _all_matches_scored_at_least(evts, 1, as_home)


def best_pick_for_match(home_id, away_id):
    h5 = get_last_events(home_id)
    a5 = get_last_events(away_id)

    info = {"home_id": home_id, "away_id": away_id,
            "samples": {"home_last": len(h5), "away_last": len(a5)}}

    ev15 = _all_matches_scored_at_least(h5, 2, True)
    dep15 = _all_matches_scored_at_least(a5, 2, False)
    kg_home = _all_matches_scored_at_least_one(h5, True)
    kg_away = _all_matches_scored_at_least_one(a5, False)
    kg = kg_home and kg_away
    over25_home = _all_matches_over_total(h5, 3)
    over25_away = _all_matches_over_total(a5, 3)
    over25 = over25_home and over25_away
    kg_over25 = kg and over25

    info["criteria"] = {"ev_1_5": ev15, "dep_1_5": dep15, "kg": kg,
                        "o2_5": over25, "kg_o2_5": kg_over25}

    if kg_over25:
        return "KG + 2.5 ÜST", info
    if ev15:
        return "Ev 1.5 ÜST", info
    if dep15:
        return "Dep 1.5 ÜST", info
    if over25:
        return "2.5 ÜST", info
    if kg:
        return "KG (Karşılıklı Gol)", info

    return None, info
