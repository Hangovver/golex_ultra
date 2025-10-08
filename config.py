# config.py
# ⚙️ API-Football + Telegram ayarları

import os

API_KEY = os.getenv("API_FOOTBALL_KEY")  # Render Environment’dan gelir
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Zamanlama
RUN_AT_HOUR = int(os.getenv("RUN_HOUR", "10"))
RUN_AT_MINUTE = int(os.getenv("RUN_MINUTE", "0"))
