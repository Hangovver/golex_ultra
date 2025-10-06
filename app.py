from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from tools.daily_runner import run_daily_analysis

app = FastAPI(title="Golex Ultra API")

scheduler = BackgroundScheduler()

@app.on_event("startup")
def startup_event():
    print("⏰ Scheduler başlatılıyor...")
    scheduler.add_job(run_daily_analysis, 'interval', hours=24, id='daily_job', replace_existing=True)
    scheduler.start()
    print("✅ Scheduler aktif.")

@app.get("/")
def home():
    return {"status": "Golex Ultra API çalışıyor."}

@app.get("/run")
def manual_run():
    print("🚀 Manuel analiz başlatıldı.")
    run_daily_analysis()
    return {"message": "Analiz başarıyla çalıştırıldı."}

atexit.register(lambda: scheduler.shutdown(wait=False))
