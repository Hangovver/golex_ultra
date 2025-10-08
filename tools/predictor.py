# tools/predictor.py
# Tahmin sistemi: KG+2.5 > Ev1.5+ > Dep1.5+ > 2.5 > KG
# Artık toleranslı (5 maçın en az 4’ünde koşulu sağlayan takım geçerli)

from tools.alt_thesportsdb import last5_home, last5_away, goals


# ------------------------------------------------------------
# 🔧 Yardımcı kurallar (toleranslı versiyon)
# ------------------------------------------------------------
def _at_least_x_of_last_n(evts: list[dict], need: int, as_home: bool, threshold=0.8) -> bool:
    """
    Belirtilen takım son N maçının en az threshold oranında (ör: %80)
    'need' kadar gol atmış mı?
    """
    if len(evts) < 3:
        return False

    good = 0
    for e in evts:
        g = goals(e)
        if not g:
            continue
        hs, aw = g
        team_goals = hs if as_home else aw
        if team_goals >= need:
            good += 1

    return good >= int(len(evts) * threshold)


def _matches_over_total(evts: list[dict], line: float, threshold=0.8) -> bool:
    """
    Maçların en az threshold oranında (ör: %80)
    toplam gol sayısı verilen çizginin üstünde mi?
    """
    if len(evts) < 3:
        return False

    good = 0
    for e in evts:
        g = goals(e)
        if not g:
            continue
        if (g[0] + g[1]) >= line:
            good += 1

    return good >= int(len(evts) * threshold)


# ------------------------------------------------------------
# 🎯 Ana tahmin fonksiyonu
# ------------------------------------------------------------
def best_pick_for_match(home: str, away: str) -> tuple[str | None, dict]:
    """
    Kurallar (son 5 maç – saha bazlı, toleranslı):
    - Ev 1.5+:    Ev takımının EVDE oynadığı son 5 maçın %80'inde ≥2 gol
    - Dep 1.5+:   Dep takımının DEPLASMANDA oynadığı son 5 maçın %80'inde ≥2 gol
    - KG:         Ev evde %80 ≥1, Dep deplasmanda %80 ≥1
    - 2.5:        Hem ev(evde) hem dep(deplasmanda) %80 toplam ≥3
    - KG+2.5:     KG şartları + 2.5 şartları birlikte

    Öncelik: KG+2.5 > Ev1.5 > Dep1.5 > 2.5 > KG
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

    # Şartlar (toleranslı)
    ev15 = _at_least_x_of_last_n(h5, 2, as_home=True)
    dep15 = _at_least_x_of_last_n(a5, 2, as_home=False)
    kg_home = _at_least_x_of_last_n(h5, 1, as_home=True)
    kg_away = _at_least_x_of_last_n(a5, 1, as_home=False)
    kg = kg_home and kg_away
    over25_home = _matches_over_total(h5, 3)
    over25_away = _matches_over_total(a5, 3)
    over25 = over25_home and over25_away
    kg_over25 = kg and over25

    info["criteria"] = {
        "ev_1_5": ev15,
        "dep_1_5": dep15,
        "kg": kg,
        "o2_5": over25,
        "kg_o2_5": kg_over25
    }

    # 🔢 Öncelik sırası
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
