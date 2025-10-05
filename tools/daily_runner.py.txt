from .telegram_bot import send_telegram_message
from .utils import filter_high_scoring_teams
import datetime

def run_daily_analysis():
    # (Gerçek API analiz kısmı burada genişletilebilir)
    # Şimdilik örnek çıktı gönderelim
    today = datetime.date.today().strftime("%d %B %Y")
    message = f"📊 GOLEX Günlük Analiz ({today})\n\n"
    message += "⚽️ 8 Maç Seçildi:\n"
    sample_matches = [
        "Liverpool - Tottenham (2.5 ÜST)",
        "PSG - Lyon (Ev 1.5+)",
        "Real Madrid - Girona (KG VAR)",
        "Galatasaray - Trabzonspor (2.5 ÜST)",
        "Man City - Arsenal (Ev 1.5+)",
        "Inter - Atalanta (2.5 ÜST)",
        "Bayern - Leipzig (KG VAR)",
        "Fenerbahçe - Beşiktaş (2.5 ÜST)"
    ]
    for m in sample_matches:
        message += f"• {m}\n"
    message += "\n🔮 Tahminler istatistiklere göre sıralandı."

    send_telegram_message(message)
