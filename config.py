# config.py
import os

# --- TheSportsDB ---
API_KEY = os.getenv("THESPORTSDB_API_KEY", "099583")
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

# --- Telegram ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8227478980:AAGF1g0PHGp6j85SG8qPyyP9hYjgfJcWyRU")
CHAT_ID = os.getenv("CHAT_ID", "5876994093")

# --- Zamanlama ---
RUN_HOUR = 10
TIMEZONE = "Europe/Istanbul"

# --- Akıllı limit ---
INITIAL_EVENT_LIMIT = 60
MIN_EVENT_LIMIT = 10
REDUCE_FACTOR = 0.8
RECOVERY_AFTER_MIN = 60
RECOVERY_GROWTH = 1.10
