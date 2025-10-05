# app.py
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

from fastapi import FastAPI
from tools.daily_runner import run_daily_analysis
from tools.scheduler import start_scheduler

# FastAPI uygulaması oluştur
app = FastAPI(title="GOLEX AI ULTRA API", version="1.0")

@app.get("/")
def root():
    """API’nin çalıştığını test etmek için"""
    return {"message": "🔥 GOLEX AI ULTRA API aktif!"}

@app.get("/run")
def manual_run():
    """Elle analiz çalıştırmak için"""
    run_daily_analysis()
    return {"status": "✅ Analiz tamamlandı ve Telegram’a gönderildi!"}


# Scheduler’ı başlat
@app.on_event("startup")
def start_background_tasks():
    print("⏰ Scheduler başlatılıyor...")
    start_scheduler()
    print("✅ Scheduler aktif.")


# Render için çalıştırma (uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
