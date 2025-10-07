# tools/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from tools.daily_runner import run_and_notify

scheduler = BackgroundScheduler()

def start_scheduler():
    """Her sabah 10:00'da analiz başlatır"""
    scheduler.add_job(run_and_notify, "cron", hour=10, minute=0)
    scheduler.start()
    print("⏰ Günlük analiz planlandı (10:00)")

def stop_scheduler():
    scheduler.shutdown()
