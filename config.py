# config.py
# ============================================
# 🔧 GOLEX Ultra - Genel Ayarlar
# TheSportsDB + Telegram entegrasyonu
# ============================================

import os

# 🔑 TheSportsDB API anahtarı
# Render ortam değişkeninde varsa onu kullanır,
# yoksa alttaki varsayılan (099583 - demo key) devreye girer.
API_KEY = os.getenv("THESPORTSDB_API_KEY", "099583")

# API adresi
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

# ============================================
# 📲 Telegram Bot Ayarları
# ============================================

# @BotFather'dan aldığın bot token
TELEGRAM_TOKEN = "8227478980:AAGF1g0PHGp6j85SG8qPyyP9hYjgfJcWyRU"

# Kendin / grubun chat ID'si
CHAT_ID = "5876994093"

# ============================================
# 🕒 Günlük Otomatik Çalışma Zamanı (UTC)
# Render sunucuları genellikle UTC saatindedir.
# Türkiye saatiyle 13:00'te çalışsın istiyorsan → 10 yap (UTC+3 farkı)
# ============================================
RUN_AT_HOUR = 10
RUN_AT_MINUTE = 0

# ============================================
# 🧠 Kontrol (opsiyonel)
# Maskelenmiş key'i terminalde gösterir (güvenli şekilde)
# ============================================
def print_masked_key():
    key = API_KEY
    masked = f"{key[:3]}...{key[-3:]}" if len(key) > 6 else key
    print(f"🔐 TheSportsDB key (masked): {masked}")

# Eğer doğrudan çalıştırılırsa test et
if __name__ == "__main__":
    print_masked_key()
