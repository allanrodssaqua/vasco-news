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

# Canal de Origem (Múltiplos)
YOUTUBE_CHANNELS = [
    {"name": "Vamo Vasco", "id": "UCF422qAj_b8ZHtKS6YUaEbg"},
    {"name": "Machão da Gama", "id": "UCS5R_abGJziuxS0rJymOvSg"}
]
# Notícias de portais parceiros
RSS_SOURCES = [
    "https://ge.globo.com/rss/futebol/times/vasco/",
    "https://www.lance.com.br/rss/vasco"
]
NEWS_FILE = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "data", "news.json")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def get_latest_video_ids(channel_id):
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    print(f"Buscando vídeos no RSS: {rss_url}")
    response = httpx.get(rss_url)
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

def generate_news_with_gemini(text, source_type="youtube", channel_name="Vasco TV"):
    if not text:
        return None
    
    prompt = f"""
    Você é Allan Rods, um curador de notícias apaixonado pelo Vasco da Gama e investigador cético.
    Sua missão é extrair fatos concretos da transcrição/dados fornecidos e criar uma matéria para sua 'Curadoria Esportiva'.

    REGRAS DE PERSONA (Allan Rods):
    1. PROIBIDO usar saudações fixas ou robotizadas. Varie a abertura em cada notícia.
    2. Use termos como: 'Saudações Vascaínas', 'Fala, torcida do Gigante', 'Allan Rods na área', 'O sentimento não pode parar', etc.
    3. O primeiro parágrafo DEVE mencionar obrigatoriamente o canal de origem ({channel_name}) e a sua 'Curadoria Esportiva', mas mude a forma de dizer isso em cada matéria para parecer humano.
    4. O tom deve ser de um jornalista que ama o clube, mas é rigoroso com os fatos.

    REGRAS JORNALÍSTICAS:
    1. PROIBIDO vagueza. Identifique quem (nomes próprios), o que (ações exatas) e quando.
    2. Se houver valores (dinheiro, tempo de contrato, placar), destaque-os.
    3. Identifique 3 pontos cruciais para a seção de Destaques.

    FORMATO DE SAÍDA (JSON):
    {{
        "title": "Título impactante e direto",
        "subtitle": "Resumo em uma frase",
        "highlights": ["Ponto crucial 1 com dado concreto", "Ponto crucial 2 com nome próprio", "Ponto crucial 3"],
        "content": "Texto completo começando com a saudação personalizada e menção à Curadoria/Canal.",
        "date": "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
        "team": "Vasco da Gama"
    }}

    Transcrição/Dados:
    {text[:10000]}
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

    # 1. Processar RSS Externos
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

    # 2. Processar Canais do YouTube
    for channel in YOUTUBE_CHANNELS:
        print(f"\n--- Processando Canal: {channel['name']} ---")
        video_ids = get_latest_video_ids(channel['id'])
        
        for v_id in video_ids:
            if v_id in existing_ids: continue
            
            print(f"Processando Vídeo: {v_id}")
            content = get_transcript(v_id)
            if not content:
                print("Transcript bloqueado. Usando metadados...")
                content = get_video_metadata(v_id)
                
            if content:
                news_data = generate_news_with_gemini(content, "youtube", channel['name'])
                if news_data:
                    news_data["source_id"] = v_id
                    news_data["source_url"] = f"https://youtube.com/watch?v={v_id}"
                    all_news.insert(0, news_data)

    # 3. Processar RSS Externos
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

    # 4. Regra de Retenção (72 horas)
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(hours=72)
    
    cleaned_news = []
    for news in all_news:
        try:
            news_date = datetime.strptime(news['date'], "%Y-%m-%d %H:%M:%S")
            if news_date > cutoff_date:
                cleaned_news.append(news)
        except:
            # Se a data estiver em formato inválido, mantemos para segurança ou removemos
            cleaned_news.append(news)

    # Salvar
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_news, f, ensure_ascii=False, indent=4)
    
    print(f"\nProcessamento concluído. Total de notícias ativas (72h): {len(cleaned_news)}")

if __name__ == "__main__":
    main()
