# tools/predictor.py
# Tek tahmin çıkarır: KG+2.5 > Ev1.5+ > Dep1.5+ > 2.5 > KG
from tools.alt_thesportsdb import last5_home, last5_away, goals

def _all_matches_scored_at_least(evts: list[dict], need: int, as_home: bool) -> bool:
    # as_home=True ise ev sahibi gol sayısına bakar; False ise deplasman golüne
    if len(evts) < 5:
        return False
    for e in evts:
        g = goals(e)
        if not g:
            return False
        hs, aw = g
        team_goals = hs if as_home else aw
        if team_goals < need:
            return False
    return True

def _all_matches_over_total(evts: list[dict], line: float) -> bool:
    if len(evts) < 5:
        return False
    for e in evts:
        g = goals(e)
        if not g:
            return False
        if (g[0] + g[1]) < line:
            return False
    return True

def _all_matches_scored_at_least_one(evts: list[dict], as_home: bool) -> bool:
    return _all_matches_scored_at_least(evts, 1, as_home)

def best_pick_for_match(home: str, away: str) -> tuple[str | None, dict]:
    """
    Kurallar (son 5 maç – saha bazlı):
    - Ev 1.5+:    Ev takımının EVDE oynadığı son 5 maçın her birinde ≥2 gol
    - Dep 1.5+:   Dep takımının DEPLASMANDA oynadığı son 5 maçın her birinde ≥2 gol
    - KG:         Ev evde son 5'te her maç ≥1, Dep deplasmanda son 5'te her maç ≥1
    - 2.5:        Hem ev(evde) hem dep(deplasmanda) son 5'te her maç toplam ≥3
    - KG+2.5:     KG şartları + 2.5 şartları birlikte

    Öncelik: KG+2.5 > Ev1.5+ > Dep1.5+ > 2.5 > KG
    """
    h5 = last5_home(home)
    a5 = last5_away(away)

    info = {
        "home": home,
        "away": away,
        "samples": {
            "home_last5_home": len(h5),
            "away_last5_away": len(a5),
        }
    }

    # Şartlar
    ev15 = _all_matches_scored_at_least(h5, 2, as_home=True)
    dep15 = _all_matches_scored_at_least(a5, 2, as_home=False)
    kg_home = _all_matches_scored_at_least_one(h5, as_home=True)
    kg_away = _all_matches_scored_at_least_one(a5, as_home=False)
    kg = kg_home and kg_away
    over25_home = _all_matches_over_total(h5, 3)
    over25_away = _all_matches_over_total(a5, 3)
    over25 = over25_home and over25_away
    kg_over25 = kg and over25

    info["criteria"] = {
        "ev_1_5": ev15,
        "dep_1_5": dep15,
        "kg": kg,
        "o2_5": over25,
        "kg_o2_5": kg_over25
    }

    # Öncelik: KG+2.5 > Ev1.5 > Dep1.5 > 2.5 > KG
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
