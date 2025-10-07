# tools/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from config import RUN_AT_HOUR, RUN_AT_MINUTE
from tools.daily_runner import run_and_notify

_scheduler = None

def start_scheduler():
    global _scheduler
    if _scheduler:
        return
    print("⏰ Zamanlayıcı başlatılıyor...")
    _scheduler = BackgroundScheduler(timezone="UTC")
    _scheduler.add_job(
        run_and_notify,
        CronTrigger(hour=RUN_AT_HOUR, minute=RUN_AT_MINUTE),
        id="daily_run",
        replace_existing=True
    )
    _scheduler.start()
    print(f"✅ Günlük analiz planlandı ({RUN_AT_HOUR:02d}:{RUN_AT_MINUTE:02d})")

def stop_scheduler():
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
