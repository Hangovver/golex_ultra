from fastapi import FastAPI
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify

app = FastAPI()

@app.on_event("startup")
def startup_event():
    """Sunucu açıldığında günlük analiz scheduler’ını başlatır."""
    print("🚀 Scheduler başlatılıyor...")
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    """Sunucu kapanırken scheduler’ı durdurur."""
    print("🛑 Scheduler durduruluyor...")
    stop_scheduler()

@app.get("/")
def home():
    """Basit kontrol sayfası."""
    return {"status": "running", "message": "GOLEX Football Analyzer aktif ✅"}

@app.get("/run")
def run_now():
    """Analizi manuel olarak hemen çalıştırır."""
    print("⚡ Manuel analiz başlatıldı...")
    run_and_notify()
    return {"status": "ok", "message": "Analiz çalıştırıldı."}
