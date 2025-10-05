from fastapi import FastAPI
import os
from tools.daily_runner import run_daily_analysis
from tools.scheduler import start_scheduler  # <-- otomatik zamanlayıcıyı çağırıyoruz

app = FastAPI()

@app.get("/")
def root():
    """API’nin çalıştığını test etmek için"""
    return {"message": "GOLEX AI ULTRA API çalışıyor 🔥"}

@app.get("/run")
def manual_run():
    """Elle analiz çalıştırmak için"""
    run_daily_analysis()
    return {"status": "Analiz tamamlandı ve Telegram’a gönderildi ✅"}

# 🕒 Scheduler başlatıcı (otomatik 11:00 gönderimi)
if __name__ == "__main__":
    start_scheduler()


