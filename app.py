from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from tools.daily_runner import run_daily_analysis

app = FastAPI(title="GOLEX Ultra", version="1.0")

# 🕒 Scheduler başlat
scheduler = BackgroundScheduler()

@app.on_event("startup")
def start_scheduler():
    print("⏰ Scheduler başlatılıyor...")
    scheduler.add_job(run_daily_analysis, "interval", hours=24, id="daily_analysis", replace_existing=True)
    scheduler.start()
    print("✅ Scheduler aktif.")

# 🧩 Manuel çalıştırma (Render’da test için)
@app.get("/run")
def run_now():
    try:
        run_daily_analysis()
        return {"status": "ok", "message": "Analiz başarıyla çalıştı."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 🏠 Basit ana sayfa
@app.get("/")
def home():
    return {"message": "GOLEX Ultra aktif. /run endpoint'i ile testi başlatabilirsiniz."}

# 🧹 Kapatılırken scheduler'ı temizle
atexit.register(lambda: scheduler.shutdown(wait=False))

