# app.py
from fastapi import FastAPI
from tools.scheduler import start_scheduler, stop_scheduler

app = FastAPI(title="GOLEX API-Football Bot")

@app.get("/")
def home():
    return {"status": "OK", "msg": "GOLEX Football Analyzer aktif!"}

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
