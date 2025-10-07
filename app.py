# app.py
from fastapi import FastAPI
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify

app = FastAPI(title="GOLEX Ultra")

@app.get("/")
def root():
    return {"ok": True, "msg": "GOLEX Ultra çalışıyor."}

@app.get("/run")
def run_now():
    # Manuel tetikleme
    run_and_notify()
    return {"ok": True, "msg": "Manuel analiz tetiklendi."}

# (Deprecation uyarıları önemli değil; Render'da iş görür)
@app.on_event("startup")
def _startup():
    start_scheduler()

@app.on_event("shutdown")
def _shutdown():
    stop_scheduler()
