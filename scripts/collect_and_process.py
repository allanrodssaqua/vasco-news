import os
import json
import httpx
import time
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Canal de Origem (Múltiplos)
YOUTUBE_CHANNELS = [
    {"name": "Vamo Vasco", "id": "UCF422qAj_b8ZHtKS6YUaEbg"},
    {"name": "Machão da Gama", "id": "UCS5R_abGJziuxS0rJymOvSg"},
    {"name": "Gigante Vasco", "id": "UCiwReSvM9QQifgkr6CW_Txw"},
    {"name": "Futbolaço_vasco", "id": "UCZ90RqFLhuwCtxKnTZbuNJg"}
]
# Configurações de Portais
PORTALS = [
    {
        "name": "GE Vasco",
        "url": "https://ge.globo.com/futebol/times/vasco/",
        "type": "ge"
    },
    {
        "name": "Lance Vasco",
        "url": "https://www.lance.com.br/vasco",
        "type": "lance"
    },
    {
        "name": "ESPN Vasco",
        "url": "https://www.espn.com.br/futebol/time/_/id/3454/vasco-da-gama",
        "type": "espn"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}
NEWS_FILE = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "data", "news.json")
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "youtube_cookies.txt")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Erro ao inicializar cliente Gemini: {e}")

import re

def get_latest_video_ids(channel_id):
    """Tenta buscar via API oficial (PlaylistItems) primeiro, fallback para scraping."""
    if YOUTUBE_API_KEY:
        try:
            # Converte Channel ID (UC...) para Uploads Playlist ID (UU...)
            playlist_id = "UU" + channel_id[2:]
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=7&key={YOUTUBE_API_KEY}"
            print(f"Buscando vídeos via API para o canal {channel_id}")
            response = httpx.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return [item['snippet']['resourceId']['videoId'] for item in data.get('items', [])]
            else:
                print(f"Erro na API YouTube ({response.status_code}). Seguindo para scraping...")
        except Exception as e:
            print(f"Falha na API YouTube: {e}. Seguindo para scraping...")

    # Fallback: Scraping
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Buscando vídeos via Scraping para o canal {channel_id} (Tentativa {attempt+1})")
            response = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
            if response.status_code != 200: 
                time.sleep(2)
                continue
            
            video_ids_found = re.findall(r'"videoId":"([^"]+)"', response.text)
            if not video_ids_found:
                time.sleep(2)
                continue

            unique_ids = []
            for vid in video_ids_found:
                if vid not in unique_ids:
                    unique_ids.append(vid)
            
            return unique_ids[:7]
        except Exception as e:
            print(f"Erro no scraping: {e}")
            time.sleep(2)
            
    return []

def get_transcript(video_id):
    """Extrai transcrição usando cookies se disponíveis para evitar 429."""
    try:
        print(f"Extraindo transcrição para o vídeo: {video_id}")
        
        # Tenta carregar cookies se o arquivo existir
        cookies_param = None
        if os.path.exists(COOKIES_FILE):
            print(f"Usando cookies de: {COOKIES_FILE}")
            cookies_param = COOKIES_FILE

        if cookies_param:
            transcript_list = YouTubeTranscriptApi().list(video_id, cookies=cookies_param)
        else:
            transcript_list = YouTubeTranscriptApi().list(video_id)
            
        try:
            transcript = transcript_list.find_transcript(['pt'])
        except:
            transcript = transcript_list.find_generated_transcript(['pt'])
            
        data = transcript.fetch()
        text = " ".join([i.text for i in data])
        return text
    except Exception as e:
        error_msg = str(e)
        if "YouTube is blocking requests from your IP" in error_msg:
            print(f"ALERTA: YouTube bloqueou o IP para transcrições. Usando apenas metadados.")
        else:
            print(f"Erro ao obter transcrição: {e}")
        return None

def get_video_metadata(video_id):
    """Busca metadados via API oficial primeiro, fallback para scraping manual."""
    if YOUTUBE_API_KEY:
        try:
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
            response = httpx.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    snippet = data['items'][0]['snippet']
                    return f"Título: {snippet['title']}\nDescrição Completa: {snippet['description']}"
        except:
            pass

    # Fallback: Scraping
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        response = httpx.get(url, follow_redirects=True, headers=HEADERS, timeout=15)
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
                    v_renderer = item.get("videoSecondaryInfoRenderer", {})
                    if v_renderer:
                        description = v_renderer.get("attributedDescription", {}).get("content", "")
                        if not description:
                            description = v_renderer.get("description", {}).get("runs", [{}])[0].get("text", "")
            except: pass
        
        if not description:
            desc_tag = soup.find("meta", attrs={"name": "description"})
            description = desc_tag["content"] if desc_tag else ""
        
        return f"Título: {title}\nDescrição Completa: {description}"
    except Exception as e:
        print(f"Erro ao obter metadados: {e}")
        return None

def generate_safe_id(url, prefix="portal"):
    import hashlib
    hash_object = hashlib.md5(url.encode())
    return f"{prefix}-{hash_object.hexdigest()[:10]}"

def get_portal_news():
    news_items = []
    for portal in PORTALS:
        try:
            print(f"Scraping Portal: {portal['name']}")
            response = httpx.get(portal['url'], headers=HEADERS, timeout=15, follow_redirects=True)
            if response.status_code != 200: continue
            soup = BeautifulSoup(response.text, "html.parser")
            
            if portal['type'] == "ge":
                items = soup.select(".feed-post")[:7]
                for item in items:
                    title_tag = item.select_one("a.feed-post-link")
                    if title_tag and title_tag.get('href'):
                        url = title_tag['href']
                        news_items.append({
                            "title": title_tag.get_text(strip=True),
                            "link": url,
                            "id": generate_safe_id(url, "ge"),
                            "source": portal['name']
                        })
            
            elif portal['type'] == "lance":
                links = soup.find_all("a", href=True)
                count = 0
                for link in links:
                    href = link['href']
                    text = link.get_text(strip=True)
                    if "/vasco/" in href and len(text) > 35:
                        full_url = f"https://www.lance.com.br{href}" if not href.startswith("http") else href
                        news_items.append({
                            "title": text,
                            "link": full_url,
                            "id": generate_safe_id(full_url, "lance"),
                            "source": portal['name']
                        })
                        count += 1
                        if count >= 7: break
            
            elif portal['type'] == "espn":
                items = soup.select("a.contentItem__content")[:7]
                for item in items:
                    title_tag = item.find(["h1", "h2"])
                    if title_tag and item.get('href'):
                        full_url = f"https://www.espn.com.br{item['href']}" if not item['href'].startswith("http") else item['href']
                        news_items.append({
                            "title": title_tag.get_text(strip=True),
                            "link": full_url,
                            "id": generate_safe_id(full_url, "espn"),
                            "source": portal['name']
                        })
                        
        except Exception as e:
            print(f"Erro no Portal {portal['name']}: {e}")
    return news_items

def generate_news_with_gemini(text, source_type="youtube", channel_name="Vasco TV"):
    if not text or not client: return None
    
    # Trunca o texto para evitar estourar o limite de contexto da API gratuita
    truncated_text = text[:30000]
    print(f"DEBUG: Enviando contexto de {len(truncated_text)} caracteres para o Gemini...")
    
    prompt = f"""
    Você é Allan Rods, um JORNALISTA ESPORTIVO INVESTIGATIVO especializado no Vasco.
    Sua missão é criar uma matéria detalhada baseada nos fatos encontrados (Nomes próprios são ESSENCIAIS).
    
    REGRA DE CONTEÚDO (CAMPO 'content'):
    - O conteúdo deve ser DETALHADO (mínimo de 3 parágrafos longos).
    - Narre os bastidores, as implicações dos fatos e a repercussão.
    - Use o estilo Allan Rods: investigativo, direto mas apaixonado pelo Vasco.
    
    Humanização: 'Saudações Vascaínas!', 'Allan Rods na área!', 'Fala, torcida do Gigante!', 'O sentimento não pode parar!'.
    Mencione o canal ({channel_name}) e sua 'CURADORIA ESPORTIVA' no início.

    FORMATO JSON (RETORNE APENAS O OBJETO):
    {{
        "title": "Título investigativo e impactante",
        "subtitle": "Resumo curto do fato principal",
        "highlights": ["Fato concreto 1 (com nomes)", "Fato concreto 2 (com nomes)", "Fato concreto 3 (com nomes)"],
        "content": "Matéria completa e detalhada em Allan Rods style. Mínimo de 600 caracteres.",
        "date": "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
        "team": "Vasco da Gama"
    }}
    CONTEÚDO PARA ANÁLISE: {truncated_text}
    """
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            data = json.loads(response.text)
            # Garante que temos um dicionário (Gemini às vezes retorna lista)
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            return data
        except Exception as e:
            if "429" in str(e):
                time.sleep((attempt + 1) * 10)
            else: 
                print(f"Erro no Gemini: {e}")
                return None
    return None

def main():
    if not GEMINI_API_KEY or not client:
        print("ERRO: GEMINI_API_KEY não configurada.")
        return

    # Limpeza de logs grandes (> 5MB)
    for log in ["debug_output.txt", "run_log.txt"]:
        log_path = os.path.join(os.path.dirname(__file__), log)
        if os.path.exists(log_path) and os.path.getsize(log_path) > 5 * 1024 * 1024:
            print(f"Limpando log grande: {log}")
            with open(log_path, "w") as f: f.write(f"Log resetado em {datetime.now()}\n")

    portal_news = get_portal_news()
    all_news = []
    if os.path.exists(NEWS_FILE):
        try:
            with open(NEWS_FILE, "r", encoding="utf-8") as f:
                all_news = json.load(f)
        except: pass

    existing_ids = [n.get("source_id") for n in all_news]

    for channel in YOUTUBE_CHANNELS:
        print(f"\n--- Canal: {channel['name']} ---")
        video_ids = get_latest_video_ids(channel['id'])
        for v_id in video_ids:
            if v_id in existing_ids: continue
            print(f"Vídeo: {v_id}")
            metadata = get_video_metadata(v_id)
            transcript = get_transcript(v_id)
            content = f"{metadata}\n\nTRANSCRIÇÃO:\n{transcript}" if transcript else metadata
            if content:
                time.sleep(10)
                news_data = generate_news_with_gemini(content, "youtube", channel['name'])
                if news_data:
                    news_data["source_id"] = v_id
                    news_data["source_url"] = f"https://youtube.com/watch?v={v_id}"
                    all_news.insert(0, news_data)
                    existing_ids.append(v_id)

    for item in portal_news:
        if item["id"] in existing_ids: continue
        print(f"Processando Portal {item['source']}: {item['title']}")
        # Delay para respeitar cota
        time.sleep(10)
        news_data = generate_news_with_gemini(f"Fonte: {item['source']}\nTítulo: {item['title']}\nLink: {item['link']}", "portal", item['source'])
        if news_data:
            news_data["source_id"] = item["id"]
            news_data["source_url"] = item["link"]
            all_news.insert(0, news_data)
            existing_ids.append(item["id"])

    # Retenção (72 horas)
    cutoff = datetime.now() - timedelta(hours=72)
    cleaned_news = []
    for news in all_news:
        try:
            if datetime.strptime(news['date'], "%Y-%m-%d %H:%M:%S") > cutoff:
                cleaned_news.append(news)
        except: cleaned_news.append(news)

    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_news, f, ensure_ascii=False, indent=4)
    
    print(f"\nConcluído. Notícias ativas (72h): {len(cleaned_news)}")

if __name__ == "__main__":
    main()
