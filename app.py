from fastapi import FastAPI
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify
import uvicorn

app = FastAPI(title="Golex Ultra", version="2.0", description="Otomatik maç analizi ve Telegram bildirimi sistemi ⚽")

@app.on_event("startup")
def startup_event():
    """Render başlatıldığında zamanlayıcıyı başlatır"""
    print("🚀 Uygulama başlatılıyor...")
    start_scheduler()
    print("✅ Zamanlayıcı aktif (her sabah 10:00)")

@app.on_event("shutdown")
def shutdown_event():
    """Render kapandığında zamanlayıcıyı durdurur"""
    print("🛑 Uygulama kapanıyor, zamanlayıcı durduruluyor...")
    stop_scheduler()

@app.get("/")
def home():
    """Durum kontrolü için basit endpoint"""
    return {
        "status": "running ✅",
        "message": "Golex Ultra aktif ve analiz planlandı ⚽",
        "manual_run": "/run"
    }

@app.get("/run")
def run_now():
    """Manuel analiz tetikleme endpoint’i"""
    print("⚡ Manuel analiz başlatıldı...")
    run_and_notify()
    return {"message": "📊 Manuel analiz tamamlandı ve Telegram’a gönderildi ✅"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
