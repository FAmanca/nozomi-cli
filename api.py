import requests
import time
import threading
from collections import deque
from config import BASE_URL


class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = threading.Lock()

    def wait(self):
        with self.lock:
            now = time.monotonic()
            while self.calls and now - self.calls[0] >= self.period:
                self.calls.popleft()
            if len(self.calls) >= self.max_calls:
                sleep_for = self.period - (now - self.calls[0])
                if sleep_for > 0:
                    time.sleep(sleep_for)
            self.calls.append(time.monotonic())


_limiter = RateLimiter(max_calls=20, period=60.0)


def _get(url, **kwargs):
    _limiter.wait()
    return requests.get(url, **kwargs)


def _memo(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


@_memo
def search(title: str) -> list:
    try:
        res = _get(f"{BASE_URL}/anime/search/{title}")
        data = res.json()
        if not data.get("ok") or "animeList" not in data.get("data", {}):
            return []
        return [{"name": a["title"], "value": a["href"]} for a in data["data"]["animeList"]]
    except Exception:
        return []

@_memo
def get_ongoing(page: int = 1) -> dict:
    try:
        res = _get(f"{BASE_URL}/anime/ongoing-anime?page={page}")
        data = res.json()
        if not data.get("ok"):
            return {}
        
        anime_list = []
        for a in data.get("data", {}).get("animeList", []):
            title = a.get("title", "Unknown")
            ep = a.get("episodes", "?")
            release = a.get("latestReleaseDate", "")
            display_name = f"{title} (Ep {ep}) - {release}"
            anime_list.append({
                "name": display_name, 
                "value": {"href": a["href"], "title": title}
            })
            
        return {
            "animeList": anime_list,
            "pagination": data.get("pagination", {})
        }
    except Exception:
        return {}


@_memo
def get_episode(href: str) -> list:
    try:
        res = _get(f"{BASE_URL}{href}")
        data = res.json()
        if not data.get("ok") or "episodeList" not in data.get("data", {}):
            return []
        episode = [{"name": a["title"], "value": a["href"]} for a in data["data"]["episodeList"]]
        return episode[::-1]
    except Exception:
        return []


@_memo
def get_qualities(href: str) -> list:
    try:
        res = _get(f"{BASE_URL}{href}")
        data = res.json()
        qualities = []
        if data.get("ok") and "downloadUrl" in data.get("data", {}):
            for q in data["data"]["downloadUrl"].get("qualities", []):
                if q.get("urls"):
                    qualities.append({"name": q["title"], "value": q["urls"]})
        return qualities
    except Exception:
        return []


def resolve_stream(url: str) -> str:
    try:
        res = requests.get(url, allow_redirects=False, timeout=10)
        redirect_url = res.headers.get("Location")
        
        if not redirect_url:
            return url
            
        if "pixeldrain.com/u/" in redirect_url:
            return redirect_url.replace("/u/", "/api/file/")
            
        # Jika dialihkan ke halaman utama otakudesu, berarti link file mati/expired
        if "otakudesu" in redirect_url.lower():
            return ""
            
        return redirect_url
    except Exception:
        return ""
