# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .daily_runner import run_daily_analysis

def start_scheduler():
    """Her gün saat 11:00'de run_daily_analysis() fonksiyonunu çalıştırır."""
    print("⏰ Scheduler başlatılıyor...")
    try:
        scheduler = BackgroundScheduler(timezone="Europe/Istanbul")

        # 🕚 Her gün saat 11:00'de analiz çalıştır
        scheduler.add_job(run_daily_analysis, 'cron', hour=11, minute=0)

        # Scheduler'ı başlat
        scheduler.start()
        print(f"✅ Scheduler aktif: {datetime.now()} itibarıyla başlatıldı.")
    except Exception as e:
        print(f"⚠️ Scheduler başlatılamadı: {e}")
