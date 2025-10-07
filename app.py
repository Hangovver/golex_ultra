# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify
import threading

app = FastAPI(title="Golex Ultra", version="1.0")

@app.get("/")
def home():
    return JSONResponse({
        "status": "running ✅",
        "message": "Golex Ultra aktif ve analiz planlandı ⚽",
        "manual_run": "/run"
    })

@app.get("/run")
def run_now():
    try:
        threading.Thread(target=run_and_notify, daemon=True).start()
        return {"message": "⚡ Manuel analiz tetiklendi (arka planda çalışıyor)"}
    except Exception as e:
        return {"error": str(e)}

@app.on_event("startup")
def startup_event():
    print("🚀 Uygulama başlatılıyor...")
    start_scheduler()
    print("✅ Zamanlayıcı aktif (her sabah 10:00)")

@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Uygulama kapatılıyor...")
    stop_scheduler()
