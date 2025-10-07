# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify
import threading

app = FastAPI(title="Golex Ultra", version="2.0 Stable AI")

@app.get("/")
def home():
    return JSONResponse({
        "status": "✅ Running",
        "message": "Golex Ultra (AI Limit Adaptation) aktif",
        "manual_run": "/run"
    })

@app.get("/run")
def run_now():
    try:
        threading.Thread(target=run_and_notify, daemon=True).start()
        return {"message": "⚡ Manuel analiz başlatıldı (arka planda)"}
    except Exception as e:
        return {"error": str(e)}

@app.on_event("startup")
def startup_event():
    print("⏰ Zamanlayıcı başlatılıyor...")
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()
