# tools/predictor.py
# 🔮 GOLEX tahmin sistemi
# Kurallar sırası: KG+2.5 > Ev1.5+ > Dep1.5+ > 2.5 > KG
# Esnek analiz: 5 maçın en az %80'i koşulu sağlıyorsa "True" kabul edilir.

from tools.alt_thesportsdb import last5_home, last5_away, goals


# ------------------------------------------------------------
# 🔧 Yardımcı Fonksiyonlar
# ------------------------------------------------------------
def _ratio_of_valid(evts: list[dict], check_fn) -> float:
    """
    Geçerli skorları baz alarak oran döndürür (0.0–1.0).
    Eksik (None) skorlu maçları saymaz.
    """
    valid = 0
    total = 0
    for e in evts:
        g = goals(e)
        if not g:
            continue  # skor yoksa geç
        total += 1
        if check_fn(g):
            valid += 1
    return valid / total if total else 0.0


def _tolerant(evts: list[dict], check_fn, threshold=0.8) -> bool:
    """
    Son maçların en az threshold oranında koşulu sağlıyorsa True.
    Örn: threshold=0.8 → %80 (5 maçın 4’ü).
    """
    if len(evts) < 3:  # örneklem azsa analiz etme
        return False
    ratio = _ratio_of_valid(evts, check_fn)
    return ratio >= threshold


# ------------------------------------------------------------
# 🎯 Ana Tahmin Fonksiyonu
# ------------------------------------------------------------
def best_pick_for_match(home: str, away: str) -> tuple[str | None, dict]:
    """
    Kurallar (toleranslı, saha bazlı analiz):
      ✅ Ev 1.5+:  Ev takımının evdeki son maçlarının %80'inde ≥2 gol
      ✅ Dep 1.5+: Dep takımının deplasmandaki son maçlarının %80'inde ≥2 gol
      ✅ KG:       Ev(evde) ve Dep(deplasmanda) %80'inde ≥1 gol
      ✅ 2.5 ÜST:  Her iki taraf da %80 oranla toplam gol ≥3
      ✅ KG+2.5:   KG ve 2.5 şartları birlikte sağlanıyorsa

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

    # 🧮 Şart kontrolleri
    ev15 = _tolerant(h5, lambda g: g[0] >= 2)
    dep15 = _tolerant(a5, lambda g: g[1] >= 2)

    kg_home = _tolerant(h5, lambda g: g[0] >= 1)
    kg_away = _tolerant(a5, lambda g: g[1] >= 1)
    kg = kg_home and kg_away

    over25_home = _tolerant(h5, lambda g: sum(g) >= 3)
    over25_away = _tolerant(a5, lambda g: sum(g) >= 3)
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
