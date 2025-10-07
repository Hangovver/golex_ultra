from fastapi import FastAPI
from tools.scheduler import start_scheduler, stop_scheduler
from tools.daily_runner import run_and_notify

app = FastAPI()

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()

@app.get("/run")
def run_now():
    run_and_notify()
    return {"status": "ok"}
