# tools/predictor.py
from typing import List, Dict, Any

def _g(v: Any) -> int:
    """Gol değerini güvenli şekilde sayıya çevirir (None, '', NaN durumlarını da 0 yapar)."""
    try:
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return 0


def analyze_match_strict(home_last5_home: List[Dict[str, Any]],
                         away_last5_away: List[Dict[str, Any]],
                         home_injuries: List[str],
                         away_injuries: List[str]) -> List[str]:
    """
    GOLEX Ultra – Katı Analiz Kuralları (Sport API Sürümü)
    ======================================================
    1️⃣ Ev 1.5 Üst  → Ev son 5 EV maçında HER BİRİNDE home_goals >= 2
    2️⃣ Dep 1.5 Üst → Dep son 5 DEP maçında HER BİRİNDE away_goals >= 2
    3️⃣ KG Var      → Ev son 5 EV maçında home_goals >= 1 VE
                      Dep son 5 DEP maçında away_goals >= 1 (HER maçta)
    4️⃣ 2.5 Üst     → Ev son 5 EV maçında toplam >= 3 VE
                      Dep son 5 DEP maçında toplam >= 3 (HER maçta)
    5️⃣ KG + 2.5 Üst→ Yukarıdakilerin tamamı aynı anda sağlanıyorsa

    + Eğer takımın as oyuncularından biri sakatsa → o takım analize dahil edilmez.
    """

    # As oyuncu sakatlığı varsa analiz dışı bırak
    if home_injuries or away_injuries:
        return ["⚠️ Önemli oyuncu sakatlığı nedeniyle analiz dışı"]

    # Güvenlik: yeterli veri yoksa boş dön
    if len(home_last5_home) < 5 or len(away_last5_away) < 5:
        return []

    H = home_last5_home[:5]
    A = away_last5_away[:5]

    def her_macta_ev_2plus(ms): return all(_g(m.get("home_goals")) >= 2 for m in ms)
    def her_macta_dep_2plus(ms): return all(_g(m.get("away_goals")) >= 2 for m in ms)
    def her_macta_ev_gol(ms): return all(_g(m.get("home_goals")) >= 1 for m in ms)
    def her_macta_dep_gol(ms): return all(_g(m.get("away_goals")) >= 1 for m in ms)
    def her_macta_ust25(ms): return all((_g(m.get("home_goals")) + _g(m.get("away_goals"))) >= 3 for m in ms)

    ev15   = her_macta_ev_2plus(H)
    dep15  = her_macta_dep_2plus(A)
    kg     = her_macta_ev_gol(H) and her_macta_dep_gol(A)
    ust25  = her_macta_ust25(H) and her_macta_ust25(A)
    kg_ust = ev15 and dep15 and ust25

    preds = []
    if ev15:  preds.append("Ev 1.5 Üst")
    if dep15: preds.append("Dep 1.5 Üst")
    if kg:    preds.append("KG Var")
    if ust25: preds.append("2.5 Üst")
    if kg_ust: preds.append("KG + 2.5 Üst")

    return preds
