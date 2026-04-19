import os
import httpx
from bs4 import BeautifulSoup
import re
import json

def get_video_metadata(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        response = httpx.get(url, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        
        title = soup.find("title").text.replace(" - YouTube", "")
        
        description = ""
        pattern = re.compile(r'var ytInitialData = ({.*?});', re.DOTALL)
        match = pattern.search(html)
        if match:
            try:
                data = json.loads(match.group(1))
                items = data.get("contents", {}).get("twoColumnWatchNextResults", {}).get("results", {}).get("results", {}).get("contents", [])
                for item in items:
                    video_renderer = item.get("videoSecondaryInfoRenderer", {})
                    if video_renderer:
                        description = video_renderer.get("attributedDescription", {}).get("content", "")
                        if not description:
                            description = video_renderer.get("description", {}).get("runs", [{}])[0].get("text", "")
            except:
                pass
        
        if not description:
            desc_tag = soup.find("meta", attrs={"name": "description"})
            description = desc_tag["content"] if desc_tag else ""
        
        return title, description
    except Exception as e:
        return None, str(e)

video_id = "eG4rL_3eXYc"
title, desc = get_video_metadata(video_id)
print(f"Title: {title}")
print(f"Description length: {len(desc)}")
print(f"Description snippet: {desc[:500]}")
