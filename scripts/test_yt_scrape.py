import httpx
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def test_youtube_scraping(channel_id):
    # Use the /videos page of the channel
    # Note: Using channel ID directly works: https://www.youtube.com/channel/{id}/videos
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    print(f"Scraping: {url}")
    try:
        response = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        print(f"Status: {response.status_code}")
        # Look for videoId in the page source
        video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
        # Remove duplicates while preserving order
        unique_ids = []
        for vid in video_ids:
            if vid not in unique_ids:
                unique_ids.append(vid)
        
        print(f"Found {len(unique_ids)} video IDs")
        for vid in unique_ids[:5]:
            print(f"- {vid}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Mario Coelho channel ID
    test_youtube_scraping("UCUzrTcQHWjvIF_XYTstdlbw")
