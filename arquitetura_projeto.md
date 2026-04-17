# Arquitetura do Projeto: Vasco News (MVP Zero Cost)

Este documento define a estrutura técnica para o agregador e gerador de notícias do Vasco, otimizado para **custo zero** de infraestrutura e processamento.

## 1. Visão Geral
O sistema opera como um pipeline serverless e estático. A coleta e o processamento de IA são realizados via GitHub Actions, que gera arquivos de dados (JSON) para serem consumidos por um frontend estático hospedado gratuitamente (Vercel ou GitHub Pages).

## 2. Tecnologias (Stack 100% Zero Cost)

### Processamento e Automação (Serverless)
- **Engine:** Python Scripts executados via **GitHub Actions**.
- **Agendamento:** Cronjob no GitHub Actions (a cada 4 horas).
- **Extração:** `google-genai` (Geing), `httpx`, `BeautifulSoup` e `youtube-transcript-api`.
- **IA:** **Google Gemini 1.5 Flash** (Free Tier via Google AI Studio).

### Armazenamento e API
- **Persistência:** Arquivos **JSON/Markdown** ou **SQLite** persistidos no próprio repositório Git.
- **API:** Não há backend ativo 24/7. O frontend consome os arquivos estáticos diretamente do repositório ou via build-time.

### Frontend
- **Core:** **Next.js 16** (Configurado para Output Estático).
- **Estilização:** Tailwind CSS v4.
- **Hospedagem:** Vercel (Plano Hobby - Gratuito).

## 3. Estrutura de Diretórios

```plaintext
Noticias/
├── .github/
│   └── workflows/
│       └── aggregator.yml    # Configuração do Cronjob (GitHub Actions)
├── scripts/
│   ├── collect_data.py       # Scraper e extração YouTube/RSS
│   ├── process_news.py       # Integração com Gemini 1.5 Flash
│   ├── requirements.txt      # google-genai, youtube-transcript-api, etc.
│   └── utils.py              # Funções auxiliares
├── data/
│   ├── news.json             # "Banco de dados" estático (output da IA)
│   └── sources.json          # URLs de canais e feeds RSS
├── frontend/                 # Projeto Next.js 16 (Static)
│   ├── src/
│   └── public/
└── arquitetura_projeto.md    # Este documento
```

## 4. Fluxo de Dados (Custo Zero)

1.  **Trigger (GitHub Actions):**
    - A cada 4 horas, o workflow `.github/workflows/aggregator.yml` é disparado.
2.  **Extração (Python Script):**
    - O script busca transcrições no canal `@vamovasco` e feeds RSS.
3.  **Geração (Gemini 1.5 Flash):**
    - O texto é enviado para o Gemini 1.5 Flash (API gratuita).
    - A IA retorna a notícia formatada em JSON.
4.  **Commit (Git Persistence):**
    - O GitHub Actions atualiza o arquivo `data/news.json`.
    - Realiza um `git commit` e `git push` de volta para o repositório.
5.  **Deploy (Frontend):**
    - O push no repositório dispara o deploy automático (Redeploy) no Vercel.
    - O frontend Next.js reconstrói as páginas estáticas com as novas notícias.

## 5. Vantagens do Modelo
- **Zero Servidor:** Sem gastos com VPS ou backend ativo.
- **Performance:** Frontend puramente estático é extremamente rápido para o usuário final.
- **Simplicidade:** Todo o controle de estado e histórico está no próprio Git.

## 6. Próximos Passos
1. Criar o script de coleta do YouTube.
2. Configurar a integração com a API do Google Gemini.
3. Definir o workflow do GitHub Actions para automação.
