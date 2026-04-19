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
    {"name": "Machão da Gama", "id": "UCS5R_abGJziuxS0rJymOvSg"},
    {"name": "Gigante Vasco", "id": "UCiwReSvM9QQifgkr6CW_Txw"},
    {"name": "Futbolaço_vasco", "id": "UCZ90RqFLhuwCtxKnTZbuNJg"},
    {"name": "Mario Coelho Vasco", "id": "UCUzrTcQHWjvIF_XYTstdlbw"}
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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Erro ao inicializar cliente Gemini: {e}")

def get_latest_video_ids(channel_id):
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        print(f"Buscando vídeos no RSS: {rss_url}")
        response = httpx.get(rss_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"Erro RSS YouTube ({response.status_code}) para o canal {channel_id}")
            return []
            
        soup = BeautifulSoup(response.content, "xml")
        video_ids = []
        for entry in soup.find_all("entry")[:3]: # Pega os 3 mais recentes
            video_id_tag = entry.find("yt:videoId")
            if video_id_tag:
                video_ids.append(video_id_tag.text)
        return video_ids
    except Exception as e:
        print(f"Erro ao acessar RSS YouTube {channel_id}: {e}")
        return []

def get_transcript(video_id):
    try:
        print(f"Extraindo transcrição para o vídeo: {video_id}")
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        try:
            transcript = transcript_list.find_transcript(['pt'])
        except:
            transcript = transcript_list.find_generated_transcript(['pt'])
            
        data = transcript.fetch()
        text = " ".join([i.text for i in data])
        
        # Opcional: Validar se a transcrição é curta demais para o esperado
        if len(text) < 500:
            print(f"Aviso: Transcrição muito curta ({len(text)} chars). Pode estar incompleta.")
            
        return text
    except Exception as e:
        error_msg = str(e)
        if "YouTube is blocking requests from your IP" in error_msg:
            print(f"ALERTA: YouTube bloqueou o IP para transcrições. Usando apenas metadados (Título/Descrição).")
        else:
            print(f"Erro ao obter transcrição: {e}")
        return None

def get_video_metadata(video_id):
    """Fallback para obter título e descrição completa via JSON interno do YouTube"""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        response = httpx.get(url, follow_redirects=True, headers=HEADERS, timeout=15)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        
        title = soup.find("title").text.replace(" - YouTube", "")
        
        # Tenta encontrar o JSON interno que contém a descrição completa
        import re
        description = ""
        pattern = re.compile(r'var ytInitialData = ({.*?});', re.DOTALL)
        match = pattern.search(html)
        if match:
            try:
                data = json.loads(match.group(1))
                # Navega no JSON complexo do YT para achar a descrição
                # Caminho comum para a descrição em JSON
                items = data.get("contents", {}).get("twoColumnWatchNextResults", {}).get("results", {}).get("results", {}).get("contents", [])
                for item in items:
                    video_renderer = item.get("videoSecondaryInfoRenderer", {})
                    if video_renderer:
                        description = video_renderer.get("attributedDescription", {}).get("content", "")
                        if not description:
                            # Fallback para formato antigo de descrição
                            description = video_renderer.get("description", {}).get("runs", [{}])[0].get("text", "")
            except:
                pass
        
        # Se falhou o JSON, tenta a meta tag tradicional
        if not description:
            desc_tag = soup.find("meta", attrs={"name": "description"})
            description = desc_tag["content"] if desc_tag else ""
        
        return f"Título: {title}\nDescrição Completa: {description}"
    except Exception as e:
        print(f"Erro ao obter metadados profundos do vídeo {video_id}: {e}")
        return None

import hashlib

def generate_safe_id(url, prefix="portal"):
    """Gera um ID seguro para URL baseado em um hash da URL original"""
    hash_object = hashlib.md5(url.encode())
    return f"{prefix}-{hash_object.hexdigest()[:10]}"

def get_portal_news():
    """Busca notícias fazendo scraping dos portais principais para evitar bloqueios de RSS"""
    news_items = []
    for portal in PORTALS:
        try:
            print(f"Scraping Portal: {portal['name']}")
            response = httpx.get(portal['url'], headers=HEADERS, timeout=15, follow_redirects=True)
            if response.status_code != 200:
                print(f"Erro ao acessar {portal['name']}: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            if portal['type'] == "ge":
                items = soup.select(".feed-post")[:5]
                for item in items:
                    title_tag = item.select_one("a.feed-post-link")
                    if title_tag and title_tag.get('href'):
                        url = title_tag['href']
                        news_items.append({
                            "title": title_tag.get_text(strip=True),
                            "link": url,
                            "id": generate_safe_id(url, "ge"),
                            "description": "",
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
                            "description": "",
                            "source": portal['name']
                        })
                        count += 1
                        if count >= 5: break
            
            elif portal['type'] == "espn":
                items = soup.select("a.contentItem__content")[:5]
                for item in items:
                    title_tag = item.find(["h1", "h2"])
                    if title_tag and item.get('href'):
                        full_url = f"https://www.espn.com.br{item['href']}" if not item['href'].startswith("http") else item['href']
                        news_items.append({
                            "title": title_tag.get_text(strip=True),
                            "link": full_url,
                            "id": generate_safe_id(full_url, "espn"),
                            "description": "",
                            "source": portal['name']
                        })
                        
        except Exception as e:
            print(f"Erro no Portal {portal['name']}: {e}")
    return news_items

def generate_news_with_gemini(text, source_type="youtube", channel_name="Vasco TV"):
    if not text:
        return None
    
    print(f"DEBUG: Enviando contexto de {len(text)} caracteres para o Gemini...")
    prompt = f"""
    Você é Allan Rods, um JORNALISTA ESPORTIVO INVESTIGATIVO especializado no Vasco.
    Sua missão principal é EXTRAIR NOMES PRÓPRIOS E FATOS CONCRETOS das informações fornecidas (Título, Descrição e Transcrição).

    REGRAS CRUCIAIS:
    1. PROIBIDO usar adjetivos genéricos (ex: 'grande reforço', 'peça vital') sem o NOME PRÓPRIO do atleta.
    2. Encontre e cite NOMES de jogadores, técnicos ou dirigentes mencionados. 
    3. Se houver discrepância entre o Título e a Transcrição, foque no que é EXPLICADO no conteúdo, mas use o Título e a Descrição como guias fundamentais de contexto.
    4. Se o conteúdo for longo, faça uma curadoria dos 3 pontos MAIS IMPACTANTES para o torcedor.
    5. NÃO seja excessivamente cético. Se a fonte cita um nome ou interesse, reporte como 'bastidores' ou 'especulação' em vez de dizer que 'não há informação'.

    REGRAS DE PERSONA (Allan Rods):
    1. HUMANIZAÇÃO: Alterne obrigatoriamente entre as seguintes saudações: 'Saudações Vascaínas!', 'Allan Rods na área!', 'Fala, torcida do Gigante!', 'O sentimento não pode parar!'.
    2. Mencione sempre o canal de origem ({channel_name}) e a sua 'CURADORIA ESPORTIVA' no primeiro parágrafo de forma natural.

    FORMATO DE SAÍDA (JSON):
    {{
        "title": "Título impactante com nomes ou fatos",
        "subtitle": "Resumo objetivo da notícia",
        "highlights": ["Fato 1", "Fato 2", "Fato 3"],
        "content": "Matéria investigativa/curadoria assinada por Allan Rods.",
        "date": "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
        "team": "Vasco da Gama"
    }}

    CONTEÚDO PARA ANÁLISE (METADADOS + TRANSCRIÇÃO):
    {text[:30000]}
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Enviando para o Gemini Flash Lite (Tentativa {attempt + 1})...")
            response = client.models.generate_content(
                model="gemini-flash-lite-latest",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait_time = (attempt + 1) * 10
                print(f"Limite de cota atingido (429). Aguardando {wait_time}s...")
                import time
                time.sleep(wait_time)
            else:
                print(f"Erro no Gemini: {e}")
                return None
    return None

def main():
    if not GEMINI_API_KEY or not client:
        print("ERRO: GEMINI_API_KEY não configurada corretamente.")
        return

    # 1. Scraping de Portais (GE, Lance, ESPN)
    portal_news = get_portal_news()

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
    import time
    for channel in YOUTUBE_CHANNELS:
        print(f"\n--- Processando Canal: {channel['name']} ---")
        try:
            # Pequeno delay entre canais
            time.sleep(1)
            video_ids = get_latest_video_ids(channel['id'])
        except Exception as e:
            print(f"Erro ao buscar vídeos do canal {channel['name']}: {e}")
            continue
            
        for v_id in video_ids:
            if v_id in existing_ids: continue
            
            print(f"Processando Vídeo: {v_id}")
            # Sempre busca metadados (Título/Descrição) para garantir contexto
            metadata = get_video_metadata(v_id)
            transcript = get_transcript(v_id)
            
            if not transcript:
                print("Transcrição não disponível. Usando apenas metadados.")
                content = metadata if metadata else None
            else:
                content = f"{metadata}\n\nTRANSCRIÇÃO COMPLETA:\n{transcript}"
                
            if content:
                # Delay para evitar limites de cota (RPM)
                # Delay aumentado para 10s para respeitar o limite de 15 RPM
                time.sleep(10)
                news_data = generate_news_with_gemini(content, "youtube", channel['name'])
                if news_data:
                    news_data["source_id"] = v_id
                    news_data["source_url"] = f"https://youtube.com/watch?v={v_id}"
                    all_news.insert(0, news_data)
                    existing_ids.append(v_id)

    # 3. Processar Notícias de Portais
    for item in portal_news:
        source_id = item["id"]  # Usa o ID seguro gerado pelo hash
        if source_id in existing_ids: continue
        
        print(f"Processando Portal {item['source']}: {item['title']}")
        content = f"Fonte: {item['source']}\nTítulo: {item['title']}\nLink: {item['link']}"
        
        # Delay de 10s para respeitar a cota do Plano Gratuito
        time.sleep(10)
        news_data = generate_news_with_gemini(content, "portal", item['source'])
        if news_data:
            news_data["source_id"] = source_id
            news_data["source_url"] = item["link"]
            all_news.insert(0, news_data)
            existing_ids.append(source_id)

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
