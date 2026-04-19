import os
import json
import httpx
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def get_transcript_info(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        print(f"Available transcripts for {video_id}:")
        for t in transcript_list:
            print(f"- Language: {t.language}, Code: {t.language_code}, Is Generated: {t.is_generated}")
            try:
                data = t.fetch()
                text = " ".join([i.text for i in data])
                print(f"  Length: {len(text)} characters")
            except Exception as e:
                print(f"  ERROR fetching transcript: {e}")
        return transcript_list
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return str(e)

# IDs de vídeos recentes de diferentes canais
test_ids = [
    {"id": "eG4rL_3eXYc", "channel": "Mario Coelho Vasco"},
    {"id": "ypFATFDiiYU", "channel": "Gigante Vasco"},
    {"id": "ClK2sR0nNSQ", "channel": "Futbolaço_vasco"}
]

for item in test_ids:
    print(f"\n--- Checking {item['channel']} ({item['id']}) ---")
    get_transcript_info(item['id'])
