# tools/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from config import RUN_AT_HOUR, RUN_AT_MINUTE
from tools.daily_runner import run_and_notify

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(run_and_notify, "cron", hour=RUN_AT_HOUR, minute=RUN_AT_MINUTE)
    scheduler.start()
    print(f"✅ Scheduler başlatıldı: {RUN_AT_HOUR}:{RUN_AT_MINUTE} UTC")

def stop_scheduler():
    scheduler.shutdown()
    print("🛑 Scheduler durduruldu.")
