from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from tools.daily_runner import run_daily_analysis
import atexit

app = FastAPI(title="Golex Ultra")

scheduler = BackgroundScheduler()

@app.get("/")
def home():
    return {"message": "Golex Ultra API aktif ✅"}

@app.get("/run")
def manual_run():
    run_daily_analysis()
    return {"message": "Analiz manuel olarak çalıştırıldı ✅"}

def start_scheduler():
    print("⏰ Scheduler başlatılıyor...")
    scheduler.add_job(run_daily_analysis, "cron", hour=12, minute=0)  # her gün 12:00
    scheduler.start()
    print("✅ Scheduler aktif.")

@app.on_event("startup")
def startup_event():
    start_scheduler()

atexit.register(lambda: scheduler.shutdown())
