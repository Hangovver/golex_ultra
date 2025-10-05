# -*- coding: utf-8 -*-
import sys, io, os
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from tools.scheduler import start_scheduler
from tools.daily_runner import run_daily_analysis

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return "<h2>🏆 GOLEX Ultra çalışıyor! 🚀</h2>"

@app.get("/run")
async def manual_run():
    try:
        run_daily_analysis()
        return {"status": "ok", "message": "Daily analysis executed successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.on_event("startup")
async def startup_event():
    print("⏰ Scheduler başlatılıyor...")
    start_scheduler()
    print("✅ Scheduler aktif.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
