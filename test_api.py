import requests

url = 'https://www.sankavollerei.web.id/anime/episode/ktmnk-episode-21-sub-indo'
res = requests.get(url).json()

if res.get('ok'):
    qualities = res['data'].get('downloadUrl', {}).get('qualities', [])
    for q in qualities:
        for u in q['urls']:
            if 'pdrain' in u['title'].lower() or 'pixel' in u['title'].lower():
                print(f"Found {q['title']} - {u['title']}: {u['url']}")
                r = requests.get(u['url'], allow_redirects=False)
                loc = r.headers.get('Location', 'No Location header')
                print(f"Redirects to: {loc}")
