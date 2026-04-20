import os
import httpx
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def test_key():
    if not YOUTUBE_API_KEY:
        print("ERRO: YOUTUBE_API_KEY não encontrada no .env")
        return

    # Teste simples: buscar informações de um canal (Vamo Vasco)
    channel_id = "UCF422qAj_b8ZHtKS6YUaEbg"
    playlist_id = "UU" + channel_id[2:]
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=1&key={YOUTUBE_API_KEY}"
    
    print(f"Testando chave com Playlist: {playlist_id}...")
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            print("SUCESSO: Chave de API do YouTube funcionando corretamente!")
            data = response.json()
            item = data.get('items', [])[0]
            print(f"Vídeo mais recente: {item['snippet']['title']}")
        else:
            print(f"FALHA: Erro {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    test_key()
