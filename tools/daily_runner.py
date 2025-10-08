# tools/daily_runner.py
import time
from datetime import date
from tools.telegram import send_telegram_message
from tools.predictor import best_pick_for_match
from tools.alt_apifootball import get_today_events

LIMIT = 60        # başlangıç üst limit
ADAPT_RATE = 0.8  # hata olursa %20 azalt
MIN_LIMIT = 10    # fazla düşmesin

def handle_api_error():
    global LIMIT
    new_limit = max(MIN_LIMIT, int(LIMIT * ADAPT_RATE))
    if new_limit < LIMIT:
        LIMIT = new_limit
        print(f"⚠️ Limit düşürüldü → {LIMIT}")

def run_and_notify():
    """Günün maçlarını al, analiz et, Telegram’a gönder."""
    global LIMIT
    print("⚡ Günlük analiz başlatıldı...")
    send_telegram_message("⚡ Günlük analiz başlatıldı...")

    try:
        matches = get_today_events()
    except Exception as e:
        print(f"⚠️ Maç listesi alınamadı: {e}")
        handle_api_error()
        send_telegram_message(f"⚠️ Maç listesi alınamadı: {e}")
        return

    results = []
    for i, m in enumerate(matches[:LIMIT]):
        home = m.get("home")
        away = m.get("away")
        if not home or not away:
            continue

        time.sleep(0.7)  # rate-limit koruması

        try:
            pick, meta = best_pick_for_match(home, away)
            if not pick or not meta:
                continue  # %70 altı güven

            results.append((home, away, pick, meta))

        except Exception as e:
            print(f"⚠️ Analiz hatası ({home}-{away}): {e}")
            time.sleep(1.5)
            continue

    # --- Rapor oluştur ---
    if not results:
        msg = (
            f"📊 <b>GOLEX Günlük Analiz ({date.today().strftime('%d %B %Y')})</b>\n\n"
            f"Bugün %70 üzeri güvenli maç bulunamadı 😅"
        )
        send_telegram_message(msg)
        print("⚠️ Uygun maç bulunamadı.")
        return

    lines = []
    for (home, away, pick, meta) in results:
        emj = "🏠" if "Ev" in pick else "🚗" if "Dep" in pick else "⚽"
        lines.append(
            f"{emj} <b>{home} – {away}</b> → <b>{pick}</b> (%{meta['confidence']} güven)\n"
            f"  • Örneklem: Ev({meta['samples']['home_last5_home']}), Dep({meta['samples']['away_last5_away']})\n"
            f"  • ev1.5:{int(meta['ratios']['ev_1_5']*100)} | dep1.5:{int(meta['ratios']['dep_1_5']*100)} | "
            f"KG:{int(meta['ratios']['kg']*100)} | 2.5:{int(meta['ratios']['o2_5']*100)} | KG+2.5:{int(meta['ratios']['kg_o2_5']*100)}"
        )

    text = (
        f"📊 <b>GOLEX Günlük Analiz ({date.today().strftime('%d %B %Y')})</b>\n\n" +
        "\n\n".join(lines)
    )

    send_telegram_message(text)
    print("✅ Analiz tamamlandı, Telegram’a gönderildi.")
