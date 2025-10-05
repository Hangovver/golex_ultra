# -*- coding: utf-8 -*-
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from tools.daily_runner import run_daily_analysis
from tools.scheduler import start_scheduler

# Lifespan yapısı: FastAPI açıldığında scheduler'ı başlatır
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏰ Scheduler başlatılıyor...")
    start_scheduler()
    print("✅ Scheduler aktif.")
    yield

# FastAPI uygulaması
app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    """API’nin çalıştığını test etmek için"""
    return {"message": "GOLEX AI ULTRA API çalışıyor 🔥"}

@app.get("/run")
def manual_run():
    """Elle analiz çalıştırmak için"""
    run_daily_analysis()
    return {"status": "Analiz tamamlandı ve Telegram’a gönderildi ✅"}


# Render’ın ana entrypoint’i
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
