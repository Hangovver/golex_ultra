# config.py
# ⚙️ Temel yapılandırma

# — TheSportsDB —
API_KEY = "099583"  # <- Premium KEY'İN (sadece örnek; kendi KEY'ini yaz)
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

# — Telegram —
TELEGRAM_TOKEN = "8227478980:AAGF1g0PHGp6j85SG8qPyyP9hYjgfJcWyRU"
CHAT_ID = "<BURAYA_CHAT_ID>"   # kullanıcı ya da grup ID

# — Zamanlama —
RUN_HOUR = 10                  # Her gün saat 10:00
TIMEZONE = "Europe/Istanbul"   # Render UTC ise saat kaymasını istemiyorsan bu alan sadece bilgi amaçlı

# — Akıllı limit —
INITIAL_EVENT_LIMIT = 60       # Günlük taranacak maksimum maç (başlangıç)
MIN_EVENT_LIMIT = 10           # En az bu seviyeye kadar düşebilir
REDUCE_FACTOR = 0.8            # 429 olursa %20 azalt
RECOVERY_AFTER_MIN = 60        # 60 dk sonra adım adım toparla (+%10)
RECOVERY_GROWTH = 1.10         # toparlanma çarpanı
