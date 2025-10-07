# tools/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from tools.daily_runner import run_and_notify

scheduler = BackgroundScheduler()

def start_scheduler():
    try:
        scheduler.add_job(run_and_notify, "cron", hour=10, minute=0, id="daily_task")
        scheduler.start()
        print("✅ Günlük analiz planlandı (10:00)")
    except Exception as e:
        print(f"⚠️ Zamanlayıcı hatası: {e}")

def stop_scheduler():
    scheduler.shutdown(wait=False)
