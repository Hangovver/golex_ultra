from fastapi import FastAPI
import os
from tools.daily_runner import run_daily_analysis
from tools.scheduler import start_scheduler

app = FastAPI()

@app.get("/")
def root():
    return {"message": "GOLEX AI ULTRA API çalışıyor 🔥"}

@app.get("/run")
def manual_run():
    """Elle analiz çalıştırmak için"""
    run_daily_analysis()
    return {"status": "Analiz tamamlandı ve Telegram’a gönderildi ✅"}

@app.on_event("startup")
def on_startup():
    print("⏰ Scheduler başlatılıyor...")
    start_scheduler()
    print("✅ Scheduler aktif.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
