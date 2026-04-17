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

# Configurações
CHANNEL_ID = "UCF422qAj_b8ZHtKS6YUaEbg" # @vamovasco
YOUTUBE_RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
# Adicionando fontes RSS extras para garantir dados
RSS_SOURCES = [
    "https://ge.globo.com/rss/futebol/times/vasco/",
    "https://www.lance.com.br/rss/vasco"
]
NEWS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "news.json")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def get_latest_video_ids():
    print(f"Buscando vídeos no RSS: {YOUTUBE_RSS_URL}")
    response = httpx.get(YOUTUBE_RSS_URL)
    soup = BeautifulSoup(response.content, "xml")
    video_ids = []
    for entry in soup.find_all("entry")[:3]: # Pega os 3 mais recentes para economizar tokens
        video_id = entry.find("yt:videoId").text
        video_ids.append(video_id)
    return video_ids

def get_transcript(video_id):
    try:
        print(f"Extraindo transcrição para o vídeo: {video_id}")
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # Tenta encontrar transcrição em português (manual ou gerada)
        try:
            transcript = transcript_list.find_transcript(['pt'])
        except:
            transcript = transcript_list.find_generated_transcript(['pt'])
            
        data = transcript.fetch()
        text = " ".join([i.text for i in data])
        return text
    except Exception as e:
        print(f"Erro ao obter transcrição: {e}")
        return None

def get_video_metadata(video_id):
    """Fallback para obter título e descrição sem transcrição"""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        response = httpx.get(url, follow_redirects=True)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title").text.replace(" - YouTube", "")
        # A descrição é mais difícil de pegar via HTML puro, mas o título já ajuda muito
        return f"Título do Vídeo: {title}"
    except:
        return None

def get_rss_news():
    """Busca notícias em feeds RSS esportivos"""
    news_items = []
    for url in RSS_SOURCES:
        try:
            print(f"Buscando RSS: {url}")
            response = httpx.get(url)
            soup = BeautifulSoup(response.content, "xml")
            for item in soup.find_all("item")[:5]:
                news_items.append({
                    "title": item.title.text,
                    "link": item.link.text,
                    "description": item.description.text if item.description else ""
                })
        except Exception as e:
            print(f"Erro no RSS {url}: {e}")
    return news_items

def generate_news_with_gemini(text, source_type="youtube"):
    if not text:
        return None
    
    prompt = f"""
    Você é um jornalista esportivo especializado no Vasco da Gama. 
    A partir da transcrição do vídeo abaixo, gere uma matéria jornalística curta e impactante.
    
    Regras:
    1. O tom deve ser profissional, mas apaixonado (estilo vascaíno).
    2. Gere um Título, um Subtítulo e o Conteúdo da matéria.
    3. O output DEVE ser um JSON válido no seguinte formato:
    {{
        "title": "Título da Matéria",
        "subtitle": "Um resumo curto",
        "content": "O texto completo da matéria",
        "date": "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
        "team": "Vasco da Gama"
    }}

    Transcrição:
    {text[:10000]}  # Limitando para não estourar o contexto
    """
    
    try:
        print("Enviando para o Gemini 3.1 Flash Lite...")
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Erro no Gemini: {e}")
        return None

def main():
    if not GEMINI_API_KEY:
        print("ERRO: GEMINI_API_KEY não encontrada no .env")
        return

    # 1. Processar YouTube
    video_ids = get_latest_video_ids()
    
    # 2. Processar RSS
    rss_news = get_rss_news()

    # Carregar notícias existentes
    if os.path.exists(NEWS_FILE):
        try:
            with open(NEWS_FILE, "r", encoding="utf-8") as f:
                all_news = json.load(f)
        except:
            all_news = []
    else:
        all_news = []

    existing_ids = [n.get("source_id") for n in all_news]

    # Processar YouTube
    for v_id in video_ids:
        if v_id in existing_ids: continue
        
        print(f"Processando Vídeo: {v_id}")
        content = get_transcript(v_id)
        if not content:
            print("Transcript bloqueado. Usando metadados...")
            content = get_video_metadata(v_id)
            
        if content:
            news_data = generate_news_with_gemini(content, "youtube")
            if news_data:
                news_data["source_id"] = v_id
                news_data["source_url"] = f"https://youtube.com/watch?v={v_id}"
                all_news.insert(0, news_data)

    # Processar RSS
    for item in rss_news:
        source_id = item["link"]
        if source_id in existing_ids: continue
        
        print(f"Processando RSS: {item['title']}")
        content = f"Título: {item['title']}\nDescrição: {item['description']}"
        news_data = generate_news_with_gemini(content, "rss")
        if news_data:
            news_data["source_id"] = source_id
            news_data["source_url"] = item["link"]
            all_news.insert(0, news_data)

    # Salvar
    all_news = all_news[:50]
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)
    
    print(f"Processamento concluído. Total de notícias: {len(all_news)}")

if __name__ == "__main__":
    main()
