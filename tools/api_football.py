import requests
import datetime
import pytz
import os

# API anahtarını ortam değişkeninden al
API_KEY = os.getenv("FOOTBALL_API_KEY")

# API adresi ve başlıklar
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

def get_today_matches(limit=30):
    try:
        # Türkiye saatine göre "bugün" tarihini al
        today = datetime.datetime.now(pytz.timezone("Europe/Istanbul")).strftime("%Y-%m-%d")

        url = f"{BASE_URL}/fixtures?date={today}"
        response = requests.get(url, headers=HEADERS)

        # Eğer API yanıtı boşsa hata fırlat
        if response.status_code != 200:
            return [f"Hata: API isteği başarısız ({response.status_code})"]

        data = response.json()
        matches = data.get("response", [])

        if not matches:
            return [f"Bugün ({today}) için maç bulunamadı."]

        match_list = []
        for match in matches[:limit]:
            league = match["league"]["name"]
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            time_utc = match["fixture"]["date"]

            # Saati Türkiye saatine çevir
            try:
                utc_time = datetime.datetime.fromisoformat(time_utc.replace("Z", "+00:00"))
                istanbul_time = utc_time.astimezone(pytz.timezone("Europe/Istanbul"))
                time_str = istanbul_time.strftime("%H:%M")
            except Exception:
                time_str = "Bilinmiyor"

            # Maç bilgisini listeye ekle
            match_list.append(f"{time_str} - {league}: {home} vs {away}")

        return match_list

    except Exception as e:
        return [f"Hata oluştu: {str(e)}"]
