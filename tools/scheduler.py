from apscheduler.schedulers.background import BackgroundScheduler
from tools.daily_runner import run_daily_analysis
import datetime

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Europe/Istanbul")

    # Her gün saat 11:00'de çalışacak
    scheduler.add_job(run_daily_analysis, "cron", hour=8, minute=0)

    scheduler.start()
    print(f"⏰ Scheduler aktif: {datetime.datetime.now()} itibarıyla başlatıldı.")
