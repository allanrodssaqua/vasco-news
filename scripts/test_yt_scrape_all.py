import httpx
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

YOUTUBE_CHANNELS = [
    {"name": "Vamo Vasco", "id": "UCF422qAj_b8ZHtKS6YUaEbg"},
    {"name": "Machão da Gama", "id": "UCS5R_abGJziuxS0rJymOvSg"},
    {"name": "Gigante Vasco", "id": "UCiwReSvM9QQifgkr6CW_Txw"},
    {"name": "Futbolaço_vasco", "id": "UCZ90RqFLhuwCtxKnTZbuNJg"},
    {"name": "Mario Coelho Vasco", "id": "UCUzrTcQHWjvIF_XYTstdlbw"}
]

def get_latest_video_ids(channel):
    url = f"https://www.youtube.com/channel/{channel['id']}/videos"
    try:
        response = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        video_ids_found = re.findall(r'"videoId":"([^"]+)"', response.text)
        unique_ids = []
        for vid in video_ids_found:
            if vid not in unique_ids:
                unique_ids.append(vid)
        print(f"Channel: {channel['name']} - Found {len(unique_ids)} unique videos. Latest: {unique_ids[0] if unique_ids else 'None'}")
        return unique_ids[:5]
    except Exception as e:
        print(f"Error for {channel['name']}: {e}")
        return []

for channel in YOUTUBE_CHANNELS:
    get_latest_video_ids(channel)
