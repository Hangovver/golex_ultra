from fastapi import FastAPI
import os
from tools.daily_runner import run_daily_analysis

app = FastAPI()

@app.get("/")
def root():
    return {"message": "GOLEX AI ULTRA API çalışıyor 🔥"}

@app.get("/run")
def manual_run():
    """Elle analiz çalıştırmak için"""
    run_daily_analysis()
    return {"status": "Analiz tamamlandı ve Telegram’a gönderildi ✅"}
