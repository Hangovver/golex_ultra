# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from .daily_runner import run_daily_analysis
import pytz
import time

def start_scheduler():
    """Scheduler'ı başlatır ve her gün 11:00'de analiz çalıştırır"""
    try:
        print("⏰ Scheduler başlatılıyor...")
        scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Istanbul"))

        # Her gün saat 11:00'de çalışacak job
        scheduler.add_job(run_daily_analysis, CronTrigger(hour=11, minute=0))

        scheduler.start()
        print(f"✅ Scheduler aktif: {datetime.now()} itibarıyla başlatıldı.")

        # Render'ın kapanmaması için sürekli açık tut (loop)
        while True:
            time.sleep(600)  # 10 dakikada bir canlı tut
    except Exception as e:
        print(f"❌ Scheduler başlatılamadı: {e}")

