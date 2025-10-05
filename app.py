from fastapi import FastAPI
import os
from tools.daily_runner import run_daily_analysis
from tools.scheduler import start_scheduler
import threading

# FastAPI uygulamasını başlat
app = FastAPI()

@app.get("/")
def root():
    return {"message": "GOLEX AI ULTRA API çalışıyor 🔥"}

@app.get("/run")
def manual_run():
    """Elle analiz çalıştırmak için"""
    run_daily_analysis()
    return {"status": "Analiz tamamlandı ve Telegram’a gönderildi ✅"}

# Scheduler'ı ayrı thread’de başlat (Render erken kapatmasın diye)
def start_bg_scheduler():
    thread = threading.Thread(target=start_scheduler, daemon=True)
    thread.start()

@app.on_event("startup")
def startup_event():
    start_bg_scheduler()

# 🚀 Render üzerinde çalıştır
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=10000)

