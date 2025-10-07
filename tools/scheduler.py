# tools/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from config import RUN_HOUR
from tools.daily_runner import run_and_notify

scheduler: BackgroundScheduler | None = None

def start_scheduler():
    global scheduler
    if scheduler:
        return scheduler
    print("⏰ Zamanlayıcı başlatılıyor...")
    scheduler = BackgroundScheduler(timezone="UTC")
    # RUN_HOUR yerel 10:00 ise UTC’de saat farkı olabilir;
    # Render genelde UTC çalışır. Basit tutuyoruz:
    scheduler.add_job(run_and_notify, CronTrigger(hour=RUN_HOUR, minute=0))
    scheduler.start()
    print(f"✅ Günlük analiz planlandı ({RUN_HOUR:02d}:00)")
    return scheduler

def stop_scheduler():
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
        print("🛑 Zamanlayıcı durduruldu.")
    scheduler = None
