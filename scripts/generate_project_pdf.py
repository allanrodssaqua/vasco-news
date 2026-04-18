import os
from fpdf import FPDF

def create_pdf():
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_title('Vasco News - Documentação Técnica')
    pdf.set_author('Allan Rods')
    
    # Add Font (supporting UTF-8)
    font_path = r'C:\Windows\Fonts\arial.ttf'
    font_bold_path = r'C:\Windows\Fonts\arialbd.ttf'
    font_italic_path = r'C:\Windows\Fonts\ariali.ttf'
    
    pdf.add_font('Arial', '', font_path)
    pdf.add_font('Arial', 'B', font_bold_path)
    pdf.add_font('Arial', 'I', font_italic_path)
    
    # Set Margins
    margin = 25
    pdf.set_left_margin(margin)
    pdf.set_right_margin(margin)
    pdf.set_auto_page_break(auto=True, margin=25)
    
    # Effective width
    eff_w = pdf.w - 2 * margin
    
    pdf.add_page()
    
    # --- TITLE PAGE ---
    pdf.set_font('Arial', 'B', 26)
    pdf.set_y(60)
    pdf.set_x(margin)
    pdf.multi_cell(eff_w, 15, 'Vasco News', align='C')
    
    pdf.ln(5)
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 18)
    pdf.multi_cell(eff_w, 10, 'Arquitetura Técnica e Operação', align='C')
    
    pdf.ln(20)
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 14)
    pdf.multi_cell(eff_w, 10, 'Relatório de Funcionamento do Projeto', align='C')
    
    pdf.set_y(180)
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(eff_w, 8, 'Autor: Allan Rods', align='C')
    pdf.set_x(margin)
    pdf.multi_cell(eff_w, 8, 'Data: 18 de Abril de 2026', align='C')
    
    # --- PAGE 2: RESUMO E TECNOLOGIAS ---
    pdf.add_page()
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(eff_w, 10, '1. Visão Geral do Projeto')
    pdf.ln(5)
    
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(eff_w, 8, (
        "O Vasco News é um portal de curadoria esportiva automatizada focado no Club de Regatas Vasco da Gama. "
        "O projeto opera como um pipeline totalmente autônomo, capturando, processando e publicando notícias "
        "com custo zero de infraestrutura e zero intervenção manual diária."
    ))
    
    pdf.ln(10)
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(eff_w, 10, '2. Pilha Tecnológica (Stack)')
    pdf.ln(5)

    def add_list_item(title, description):
        pdf.set_x(margin)
        pdf.set_font('Arial', 'B', 12)
        pdf.multi_cell(eff_w, 8, f'• {title}')
        pdf.set_x(margin)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(eff_w, 8, description)
        pdf.ln(6)

    add_list_item('Frontend: Next.js 16 & Tailwind CSS v4', 
                 "Interface estática hospedada na Vercel, garantindo performance extrema e SEO de alta qualidade.")
    
    add_list_item('Inteligência Artificial: Google Gemini 3.1 Flash Lite', 
                 "Utilizado para 'Curadoria Esportiva'. A IA analisa transcrições e metadados de vídeos em busca de fatos e nomes próprios, escrevendo notícias com o tom de voz do jornalista Allan Rods.")
    
    add_list_item('Monitoramento: 5 Canais YouTube e feeds RSS', 
                 "O sistema monitora em tempo real: Vamo Vasco, Machão da Gama, Gigante Vasco, Futbolaço e Mario Coelho, além de portais como GE e Lance.")
    
    add_list_item('Automação: GitHub Actions', 
                 "Executa o pipeline completo a cada 1 hora. Realiza a coleta, gera os dados e atualiza o site automaticamente.")

    # --- PAGE 3: FLUXO E OPERAÇÃO ---
    pdf.add_page()
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(eff_w, 10, '3. Fluxo de Funcionamento e Conexões')
    pdf.ln(5)
    
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(eff_w, 8, (
        "O funcionamento do sistema segue um pipeline linear de 4 etapas:\n\n"
        "1. Coleta: O script consulta os feeds XML dos canais monitorados. Se detecta um vídeo novo (não processado anteriormente), inicia a extração de dados.\n\n"
        "2. Processamento: O sistema tenta obter a transcrição do vídeo. Caso o YouTube bloqueie a transcrição, o script faz um fallback para os metadados (título e descrição completa). Esses dados são enviados ao Gemini 3.1 Flash Lite.\n\n"
        "3. Persistência: A IA retorna um JSON estruturado. O script insere essa nova notícia no topo do arquivo 'news.json' e aplica a regra de retenção de 72 horas (removendo notícias antigas).\n\n"
        "4. Deploy: O GitHub Actions realiza o commit dos novos dados no repositório. Esse push dispara automaticamente o deploy na Vercel, que reconstrói as páginas estáticas em poucos segundos."
    ))

    pdf.ln(20)
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 14)
    pdf.multi_cell(eff_w, 10, 'Conclusão')
    pdf.ln(5)
    pdf.set_x(margin)
    pdf.set_font('Arial', 'I', 12)
    pdf.multi_cell(eff_w, 8, "O Vasco News é uma demonstração de eficiência tecnológica, unindo curadoria humana (via IA especializada) e automação serverless. O sistema garante que a torcida vascaína tenha acesso às notícias dos principais influenciadores do clube em uma única plataforma, de forma rápida e organizada.")

    output_path = 'Vasco_News_Documentacao.pdf'
    pdf.output(output_path)
    print(f"PDF gerado com sucesso em: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_pdf()
