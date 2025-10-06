from fastapi import FastAPI
from tools.daily_runner import run_daily_analysis
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = FastAPI(title="GOLEX Ultra Bot", version="2.0")

scheduler = BackgroundScheduler()

@app.on_event("startup")
def startup_event():
    try:
        scheduler.add_job(run_daily_analysis, "cron", hour=8, minute=0)
        scheduler.start()
        print("✅ Scheduler başlatıldı.")
    except Exception as e:
        print(f"⚠️ Scheduler başlatılamadı: {e}")

atexit.register(lambda: scheduler.shutdown(wait=False))

@app.get("/")
def home():
    return {"status": "GOLEX Bot çalışıyor 🚀"}

@app.get("/run")
def manual_run():
    run_daily_analysis()
    return {"status": "Manuel analiz gönderildi ✅"}

