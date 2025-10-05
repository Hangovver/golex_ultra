from fastapi import FastAPI
import os
import sys
import io
from tools.daily_runner import run_daily_analysis
from tools.scheduler import start_scheduler

# UTF-8 stdout (latin-1 hatalarını önler)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# FastAPI uygulaması
app = FastAPI()

@app.get("/")
def root():
    """API test endpointi"""
    return {"message": "🔥 GOLEX ULTRA API aktif ve çalışıyor!"}

@app.get("/run")
def manual_run():
    """Elle analiz çalıştırmak için"""
    try:
        run_daily_analysis()
        return {"status": "✅ Analiz tamamlandı ve Telegram’a gönderildi!"}
    except Exception as e:
        print(f"⚠️ Manuel çalıştırma hatası: {e}")
        return {"error": str(e)}

# 🚀 Scheduler’ı başlat (FastAPI açıldığında otomatik devreye girer)
@app.on_event("startup")
def start_scheduled_job():
    print("⏰ Scheduler başlatılıyor...")
    start_scheduler()
    print("✅ Scheduler aktif.")

# Render üzerinde app'i çalıştır
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
