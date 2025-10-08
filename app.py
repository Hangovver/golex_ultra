# app.py
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify

app = FastAPI(title="GOLEX Ultra")

@app.get("/", response_class=PlainTextResponse)
def root():
    return "✅ GOLEX Ultra çalışıyor.\n/run ile manuel analiz tetikleyebilirsin."

@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"

@app.get("/run", response_class=PlainTextResponse)
def run_now():
    """Manuel analiz tetikleme (Telegram’a da gönderir)."""
    print("⚡ Manuel analiz başlatıldı...")
    run_and_notify()
    return "Manuel analiz tamamlandı ve Telegram’a gönderildi ✅"

# ⚙️ Scheduler (her gün RUN_HOUR'da otomatik çalışır)
@app.on_event("startup")
def _startup():
    print("✅ Scheduler başlatılıyor...")
    start_scheduler()

@app.on_event("shutdown")
def _shutdown():
    stop_scheduler()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
