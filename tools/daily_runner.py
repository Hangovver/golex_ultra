# tools/daily_runner.py
import time
from datetime import datetime, timedelta
from config import (
    INITIAL_EVENT_LIMIT, MIN_EVENT_LIMIT,
    REDUCE_FACTOR, RECOVERY_AFTER_MIN, RECOVERY_GROWTH
)
from tools.alt_thesportsdb import get_today_events
from tools.predictor import best_pick_for_match
from tools.telegram import send_message_markdown

# Dinamik limit (akıllı dengeleme)
_current_limit = INITIAL_EVENT_LIMIT
_last_reduce_ts = None

def _reduce_limit():
    global _current_limit, _last_reduce_ts
    new_limit = max(MIN_EVENT_LIMIT, int(_current_limit * REDUCE_FACTOR))
    if new_limit < _current_limit:
        _current_limit = new_limit
        _last_reduce_ts = datetime.utcnow()
        print(f"⚠️ Limit düşürüldü → {_current_limit}")

def _maybe_recover_limit():
    global _current_limit, _last_reduce_ts
    if not _last_reduce_ts:
        return
    if datetime.utcnow() - _last_reduce_ts >= timedelta(minutes=RECOVERY_AFTER_MIN):
        new_limit = int(_current_limit * RECOVERY_GROWTH)
        # tavanı çok zorlamayalım: INITIAL_EVENT_LIMIT’i aşmasın
        if new_limit > INITIAL_EVENT_LIMIT:
            new_limit = INITIAL_EVENT_LIMIT
        if new_limit != _current_limit:
            _current_limit = new_limit
            print(f"🔄 Limit toparlandı → {_current_limit}")
        # tekrar saymaya başla
        _last_reduce_ts = datetime.utcnow()

def _pick_to_emoji(pick: str | None) -> str:
    return {
        "KG + 2.5 ÜST": "🔥",
        "Ev 1.5 ÜST": "🏠",
        "Dep 1.5 ÜST": "🛫",
        "2.5 ÜST": "⚽️",
        "KG (Karşılıklı Gol)": "🔁",
        None: "❌",
    }.get(pick, "❌")

def build_report(matches: list[tuple[str, dict]]) -> str:
    day = datetime.utcnow().strftime("%d %B %Y")
    lines = [f"📊 *GOLEX Günlük Analiz* ({day})", ""]
    if not matches:
        lines.append("Bugün uygun maç bulunamadı 😅")
        return "\n".join(lines)

    for pick, meta in matches:
        home = meta["home"]; away = meta["away"]
        emj = _pick_to_emoji(pick)
        crit = meta["criteria"]
        lines.append(
            f"{emj} *{home} – {away}* → *{pick or '—'}*\n"
            f"  • Örneklem: Ev({meta['samples']['home_last5_home']}), Dep({meta['samples']['away_last5_away']})\n"
            f"  • [ev1.5:{'✓' if crit['ev_1_5'] else '✗'} | dep1.5:{'✓' if crit['dep_1_5'] else '✗'} | KG:{'✓' if crit['kg'] else '✗'} | 2.5:{'✓' if crit['o2_5'] else '✗'} | KG+2.5:{'✓' if crit['kg_o2_5'] else '✗'}]"
        )
    return "\n".join(lines)

def run_daily_analysis() -> list[tuple[str, dict]]:
    """
    Günün maçlarını çeker, her maç için *tek* en uygun tahmini üretir.
    Akıllı limit çalışır; 429 gelirse limit düşer.
    """
    global _current_limit
    _maybe_recover_limit()

    try:
        events = get_today_events(limit=_current_limit)
    except Exception as e:
        # muhtemel 429 veya ağ
        print(f"⚠️ Maç listesi alınamadı: {e}")
        _reduce_limit()
        events = []

    results: list[tuple[str, dict]] = []

    for ev in events:
        home = (ev.get("strHomeTeam") or "").strip()
        away = (ev.get("strAwayTeam") or "").strip()
        if not home or not away:
            continue

        try:
            pick, info = best_pick_for_match(home, away)
            if pick:
                results.append((pick, info))
        except Exception as e:
            # tek maç özelinde limit/429 vs olabilir
            print(f"⚠️ Analiz hatası ({home}-{away}): {e}")
            # çok art arda olursa global limiti düşürelim
            _reduce_limit()
            # ufak bir bekleme
            time.sleep(1)

    return results

def run_and_notify():
    print("⚡ Günlük analiz başlatıldı...")
    matches = run_daily_analysis()
    report = build_report(matches)
    send_message_markdown(report)
