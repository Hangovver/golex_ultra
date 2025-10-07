# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify
import threading

app = FastAPI(title="Golex Ultra", version="1.0")

# 🧩 Ana sayfa (durum kontrolü)
@app.get("/")
def home():
    return JSONResponse({
        "status": "running ✅",
        "message": "Golex Ultra aktif ve analiz planlandı ⚽",
        "manual_run": "/run"
    })

# ⚡ Manuel analiz (kullanıcı tarayıcıdan çağırır)
@app.get("/run")
def run_now():
    try:
        # Analizi ayrı thread’de çalıştır, API’yi bloklamasın
        threading.Thread(target=run_and_notify, daemon=True).start()
        return {"message": "⚡ Manuel analiz tetiklendi (arka planda çalışıyor)"}
    except Exception as e:
        return {"error": str(e)}

# 🔁 Render başlarken çalışacak
@app.on_event("startup")
def startup_event():
    print("🚀 Uygulama başlatılıyor...")
    start_scheduler()
    print("✅ Zamanlayıcı aktif (her sabah 10:00)")

# 📴 Render kapanırken
@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Uygulama kapatılıyor...")
    stop_scheduler()
