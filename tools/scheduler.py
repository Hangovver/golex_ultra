from apscheduler.schedulers.background import BackgroundScheduler
from tools.daily_runner import run_and_notify

scheduler = BackgroundScheduler()

def start_scheduler():
    """Her sabah saat 10:00’da otomatik çalıştırır"""
    scheduler.add_job(run_and_notify, "cron", hour=10, minute=0)
    scheduler.start()
    print("⏰ Günlük analiz planlandı (10:00)")

def stop_scheduler():
    """Zamanlayıcıyı durdurur"""
    scheduler.shutdown()
    print("🛑 Zamanlayıcı durduruldu")
