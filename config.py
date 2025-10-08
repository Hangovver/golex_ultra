# config.py
# ⚙️ Temel yapılandırma

# — API-Football —
API_FOOTBALL_KEY = "e2b833f49d4426fc68951f537e21ade9"  # Render'da environment'tan çekilecek
BASE_URL_FOOTBALL = "https://v3.football.api-sports.io"

# — Telegram —
TELEGRAM_TOKEN = "8227478980:AAGF1g0PHGp6j85SG8qPyyP9hYjgfJcWyRU"
CHAT_ID = "5876994093"

# — Zamanlama —
RUN_HOUR = 10
TIMEZONE = "Europe/Istanbul"

# — Akıllı limit —
INITIAL_EVENT_LIMIT = 60
MIN_EVENT_LIMIT = 10
REDUCE_FACTOR = 0.8
RECOVERY_AFTER_MIN = 60
RECOVERY_GROWTH = 1.10
