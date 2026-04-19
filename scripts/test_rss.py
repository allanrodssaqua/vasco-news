import httpx

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SOURCES = [
    "https://ge.globo.com/rss/futebol/times/vasco/",
    "https://www.lance.com.br/rss/vasco",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCUzrTcQHWjvIF_XYTstdlbw"
]

for url in SOURCES:
    try:
        print(f"Testing {url}...")
        response = httpx.get(url, headers=HEADERS, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Length: {len(response.content)}")
    except Exception as e:
        print(f"Error: {e}")
