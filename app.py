from fastapi import FastAPI
import uvicorn
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("⏰ Scheduler başlatılıyor...")
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Scheduler durduruluyor...")
    stop_scheduler()

@app.get("/")
def home():
    return {"status": "running", "message": "GOLEX Football Analyzer aktif ✅"}

@app.get("/run")
def run_now():
    print("⚡ Manuel analiz başlatıldı...")
    run_and_notify()
    return {"status": "ok", "message": "Analiz çalıştırıldı."}

# Render otomatik olarak gunicorn ile calistirmazsa
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
