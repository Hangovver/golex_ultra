import os
from tools.alt_thesportsdb import get_today_events, get_team_id_by_name, get_last_5_matches
from tools.telegram import send_telegram_message

def analyze_team(team_name: str):
    team_id = get_team_id_by_name(team_name)
    if not team_id:
        return None

    matches = get_last_5_matches(team_id)
    if not matches:
        return None

    team_goals_each, opp_goals_each, totals_each, kg_each = [], [], [], []

    for m in matches:
        try:
            h = int(m.get("intHomeScore", 0) or 0)
            a = int(m.get("intAwayScore", 0) or 0)
            home = (m.get("strHomeTeam") or "").lower()
            away = (m.get("strAwayTeam") or "").lower()
            t = team_name.lower()

            if t in home:
                g_for, g_opp = h, a
            elif t in away:
                g_for, g_opp = a, h
            else:
                continue

            team_goals_each.append(g_for)
            opp_goals_each.append(g_opp)
            totals_each.append(h + a)
            kg_each.append(h > 0 and a > 0)
        except Exception:
            continue

    if not team_goals_each:
        return None

    every_match_2plus = all(g >= 2 for g in team_goals_each)
    kg_all_5 = all(kg_each)
    over25_all_5 = all(t >= 3 for t in totals_each)

    return {
        "team": team_name,
        "every_2plus": every_match_2plus,
        "kg_all_5": kg_all_5,
        "over25_all_5": over25_all_5,
        "avg_for": sum(team_goals_each) / len(team_goals_each),
        "avg_total": sum(totals_each) / len(totals_each),
    }

def analyze_match(home, away):
    h = analyze_team(home)
    a = analyze_team(away)
    if not h or not a:
        return None

    ev15 = h["every_2plus"]
    dep15 = a["every_2plus"]
    kg = h["kg_all_5"] and a["kg_all_5"]
    ust25 = h["over25_all_5"] and a["over25_all_5"]
    kgust = kg and ust25

    return {
        "match": f"{home} vs {away}",
        "EV 1.5+": ev15,
        "DEP 1.5+": dep15,
        "KG": kg,
        "ÜST 2.5": ust25,
        "KG+ÜST": kgust,
        "home_avg": round(h["avg_for"], 2),
        "away_avg": round(a["avg_for"], 2),
    }

def run_and_notify():
    events = get_today_events()
    if not events:
        send_telegram_message("⚽️ Bugün maç bulunamadı.")
        return

    lines = ["📊 *GOLEX Günlük Analiz*"]
    for e in events:
        home, away = e.get("strHomeTeam"), e.get("strAwayTeam")
        if not home or not away:
            continue
        r = analyze_match(home, away)
        if not r:
            continue
        tick = lambda x: "✅" if x else "❌"
        lines.append(
            f"\n*{r['match']}*\n"
            f"EV 1.5+: {tick(r['EV 1.5+'])} | DEP 1.5+: {tick(r['DEP 1.5+'])}\n"
            f"KG: {tick(r['KG'])} | ÜST 2.5: {tick(r['ÜST 2.5'])} | KG+ÜST: {tick(r['KG+ÜST'])}\n"
            f"_(Ev Ort: {r['home_avg']}  Dep Ort: {r['away_avg']})_"
        )

    send_telegram_message("\n".join(lines))
