from fastapi import FastAPI
import os
from tools.daily_runner import run_daily_analysis

# FastAPI uygulamasını başlatıyoruz
app = FastAPI()

@app.get("/")
def root():
    """API’nin çalıştığını test etmek için"""
    return {"message": "GOLEX AI ULTRA API çalışıyor 🔥"}

@app.get("/run")
def manual_run():
    """Elle analiz çalıştırmak için"""
    run_daily_analysis()
    return {"status": "Analiz tamamlandı ve Telegram’a gönderildi ✅"}


# 🚀 Uygulamanın Render üzerinde sürekli açık kalmasını sağlar
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
