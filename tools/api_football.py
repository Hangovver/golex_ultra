import requests
import datetime
import os

# ⚙️ API Football ayarları
API_KEY = os.getenv("FOOTBALL_API_KEY", "BURAYA_API_KEYİNİ_YAZ")  # Render Environment Variable'dan okur
BASE_URL = "https://v3.football.api-sports.io"

def get_today_matches():
    """
    Bugünkü futbol maçlarını çeker ve okunabilir liste olarak döndürür.
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/fixtures?date={today}"

    headers = {
        "x-apisports-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        matches = []
        for match in data.get("response", []):
            fixture = match.get("fixture", {})
            league = match.get("league", {}).get("name", "Lig Bilinmiyor")
            home = match.get("teams", {}).get("home", {}).get("name", "Ev Sahibi")
            away = match.get("teams", {}).get("away", {}).get("name", "Deplasman")
            time = fixture.get("date", "")[11:16]  # Sadece saat kısmını al

            matches.append(f"{time} — {home} vs {away} ({league})")

        if not matches:
            return ["Bugün maç bulunamadı ⚽️"]

        return matches

    except requests.exceptions.Timeout:
        print("⚠️ API isteği zaman aşımına uğradı.")
        return ["API isteği zaman aşımına uğradı."]
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API isteği başarısız: {e}")
        return [f"API isteği başarısız: {e}"]
    except Exception as e:
        print(f"⚠️ Genel hata: {e}")
        return [f"Hata oluştu: {e}"]
