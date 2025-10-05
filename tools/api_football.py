# -*- coding: utf-8 -*-
import requests
import datetime
import random
import sys, io

# UTF-8 karakter desteği (Render’da emoji/simge hatasını engeller)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

# 🔑 API Football Key (kendi key’ini buraya yaz)
API_KEY = "YOUR_API_KEY_HERE"
API_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

HEADERS = {
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
    "X-RapidAPI-Key": API_KEY
}

# Tahmin seçenekleri
PREDICTIONS = ["2.5 ÜST", "Ev 1.5+", "Dep 1.5+", "KG VAR"]

def get_today_matches():
    """Bugünün maçlarını döndürür (maksimum 30 tane, tahminlerle birlikte)."""
    try:
        today = datetime.date.today().strftime("%Y-%m-%d")
        params = {"date": today, "timezone": "Europe/Istanbul"}
        response = requests.get(API_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            return [f"Hata: API yanıtı {response.status_code}"]

        data = response.json()
        fixtures = data.get("response", [])

        matches = []
        for match in fixtures[:30]:
            try:
                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]
                league = match["league"]["name"]

                # Tahmini rastgele seç
                prediction = random.choice(PREDICTIONS)

                # Saat kaldırıldı, sadece lig + maç + tahmin
                matches.append(f"{league}: {home} - {away} ({prediction})")
            except Exception:
                continue

        if not matches:
            return ["Bugün maç bulunamadı 😅"]

        return matches

    except Exception as e:
        return [f"Hata oluştu: {e}"]
