import httpx
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

def test_ge_scraping():
    url = "https://ge.globo.com/futebol/times/vasco/"
    print(f"\nTesting GE Scraping: {url}")
    try:
        response = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        print(f"Status: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".feed-post")
        print(f"Items found: {len(items)}")
        for item in items[:3]:
            title_tag = item.select_one("a.feed-post-link")
            if title_tag:
                print(f"- Title: {title_tag.get_text(strip=True)}")
                print(f"- Link: {title_tag['href']}")
    except Exception as e:
        print(f"GE Error: {e}")

def test_lance_scraping():
    url = "https://www.lance.com.br/vasco"
    print(f"\nTesting Lance Scraping: {url}")
    try:
        response = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        print(f"Status: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        # Lance usa classes JSX dinâmicas, vamos tentar encontrar links de notícias
        items = soup.find_all("a", href=True)
        count = 0
        for item in items:
            href = item['href']
            if "/vasco/" in href and len(item.get_text()) > 30:
                print(f"- Title: {item.get_text(strip=True)}")
                print(f"- Link: https://www.lance.com.br{href}" if not href.startswith("http") else href)
                count += 1
                if count >= 3: break
    except Exception as e:
        print(f"Lance Error: {e}")

def test_espn_scraping():
    url = "https://www.espn.com.br/futebol/time/_/id/3454/vasco-da-gama"
    print(f"\nTesting ESPN Scraping: {url}")
    try:
        response = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        print(f"Status: {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select("section.col-three a.contentItem__content")
        if not items:
            items = soup.select("a.contentItem__content")
        print(f"Items found: {len(items)}")
        for item in items[:3]:
            title = item.find(["h1", "h2"])
            if title:
                print(f"- Title: {title.get_text(strip=True)}")
                print(f"- Link: https://www.espn.com.br{item['href']}" if not item['href'].startswith("http") else item['href'])
    except Exception as e:
        print(f"ESPN Error: {e}")

if __name__ == "__main__":
    test_ge_scraping()
    test_lance_scraping()
    test_espn_scraping()
