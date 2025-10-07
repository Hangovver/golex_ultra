# tools/alt_thesportsdb.py
import requests
import time
from config import API_KEY, BASE_URL
from tools.telegram import send_message

# Başlangıç ayarları
MAX_MATCHES = 50        # ilk limit
MIN_MATCHES = 10        # minimum limit
RECOVERY_STEP = 5       # 1 saat sonra artış miktarı
SLEEP_TIME = 10         # 429 hatasında bekleme süresi
_last_limit_reduction = 0

def _get(endpoint, params=None):
    """API isteği (adaptif limit kontrollü)"""
    url = f"{BASE_URL}/{endpoint}"
    headers = {"User-Agent": "Golex-Ultra/2.0"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        if r.status_code == 200:
            time.sleep(1.2)
            return r.json()
        elif r.status_code == 429:
            print(f"⚠️ Too many requests — {SLEEP_TIME} saniye bekleniyor...")
            time.sleep(SLEEP_TIME)
            return {"error": "rate_limit"}
        else:
            print(f"❌ API hatası: {r.status_code} - {r.text}")
            return None
    except Exception as e:
        print(f"❌ API bağlantı hatası: {e}")
        time.sleep(5)
        return None


def get_team_id_by_name(team_name: str):
    data = _get("searchteams.php", {"t": team_name})
    if not data or not data.get("teams"):
        print(f"⚠️ Takım bulunamadı: {team_name}")
        return None
    return data["teams"][0]["idTeam"]


def get_last_5_matches(team_id: str):
    data = _get("eventslast.php", {"id": team_id})
    if not data or not data.get("results"):
        return []
    return data["results"][:5]


def get_today_events():
    """Bugünün maçlarını çeker, limit otomatik ayarlanır."""
    global MAX_MATCHES, _last_limit_reduction
    data = _get("eventsday.php", {"d": time.strftime("%Y-%m-%d")})
    if not data or not data.get("events"):
        print("⚠️ Bugün için maç bulunamadı.")
        return []

    events = data["events"][:MAX_MATCHES]
    if data.get("error") == "rate_limit":
        if MAX_MATCHES > MIN_MATCHES:
            MAX_MATCHES = max(int(MAX_MATCHES * 0.8), MIN_MATCHES)
            _last_limit_reduction = time.time()
            send_message(f"⚠️ API limiti aşıldı, maç sayısı {MAX_MATCHES}’a düşürüldü.")
            print(f"⚠️ Yeni limit: {MAX_MATCHES}")
        return []

    # Eğer 1 saat geçmişse limit artır
    if _last_limit_reduction and (time.time() - _last_limit_reduction > 3600):
        MAX_MATCHES = min(MAX_MATCHES + RECOVERY_STEP, 80)
        send_message(f"✅ Limit toparlandı, maç sayısı {MAX_MATCHES}’a çıkarıldı.")
        _last_limit_reduction = 0

    return events
