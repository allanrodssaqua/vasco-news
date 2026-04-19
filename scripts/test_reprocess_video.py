import os
import json
import sys
from datetime import datetime

# Adiciona o diretório atual ao path para importar o script principal
sys.path.append(os.path.dirname(__file__))
import collect_and_process as cp

def test_specific_video(video_id, channel_name):
    print(f"\n--- TESTE DE REPROCESSAMENTO: {video_id} ({channel_name}) ---")
    
    # Busca metadados e transcrição
    metadata = cp.get_video_metadata(video_id)
    transcript = cp.get_transcript(video_id)
    
    if not transcript:
        print("Transcrição não disponível. Usando apenas metadados.")
        content = metadata
    else:
        print(f"Transcrição obtida: {len(transcript)} caracteres.")
        content = f"{metadata}\n\nTRANSCRIÇÃO COMPLETA:\n{transcript}"
    
    # Gera notícia com Gemini
    news_data = cp.generate_news_with_gemini(content, "youtube", channel_name)
    
    if news_data:
        print("\n--- RESULTADO DO GEMINI ---")
        print(json.dumps(news_data, indent=4, ensure_ascii=False))
        
        # Opcional: Salvar em um arquivo temporário para conferência
        with open("test_result.json", "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)
    else:
        print("\nERRO: Gemini não retornou dados.")

if __name__ == "__main__":
    video_id = "eG4rL_3eXYc"
    channel_name = "Mario Coelho Vasco"
    test_specific_video(video_id, channel_name)
