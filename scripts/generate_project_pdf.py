import os
from fpdf import FPDF

def create_pdf():
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_title('Vasco News - Estratégia')
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
    pdf.multi_cell(eff_w, 10, 'Arquitetura Técnica, Estratégia e Monetização', align='C')
    
    pdf.ln(20)
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 14)
    pdf.multi_cell(eff_w, 10, 'Documento de Planejamento Estratégico', align='C')
    
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
        "O projeto nasceu com a premissa de 'Custo Zero' de infraestrutura, utilizando o que há de mais moderno em "
        "automação serverless e inteligência artificial para entregar notícias verificadas e humanizadas em tempo real."
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
                 "Interface estática otimizada para velocidade de carregamento instantâneo e SEO (Core Web Vitals).")
    
    add_list_item('Inteligência Artificial: Google Gemini 1.5 Flash', 
                 "Responsável pela 'Curadoria Esportiva', transformando transcrições de vídeos e feeds de notícias em textos jornalísticos com persona própria.")
    
    add_list_item('Automação: GitHub Actions', 
                 "Orquestrador que executa o pipeline de coleta a cada 4 horas, garantindo atualização constante sem intervenção humana.")
    
    add_list_item('Hospedagem: Vercel', 
                 "Plataforma global para entrega do conteúdo estático com baixa latência.")

    # --- PAGE 3: FLUXO E CONEXÕES ---
    pdf.add_page()
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(eff_w, 10, '3. Fluxo de Funcionamento e Conexões')
    pdf.ln(5)
    
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(eff_w, 8, (
        "O funcionamento do sistema segue um pipeline linear de 4 etapas:\n\n"
        "1. Coleta: O sistema se conecta às APIs do YouTube e feeds RSS de canais especializados (ex: Vamo Vasco, Machão da Gama).\n\n"
        "2. Processamento: As transcrições e textos brutos são enviados para o modelo Gemini 1.5 Flash, que filtra o 'ruído' e extrai apenas informações relevantes.\n\n"
        "3. Persistência: Os dados processados são salvos em arquivos JSON que servem como o banco de dados estático do portal.\n\n"
        "4. Disponibilização: O GitHub Actions realiza um commit dos novos dados, o que dispara um rebuild automático no Vercel, publicando as notícias."
    ))

    # --- PAGE 4: PLANO DE MELHORIAS ---
    pdf.add_page()
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(eff_w, 10, '4. Plano de Melhorias Técnicas')
    pdf.ln(5)
    
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(eff_w, 8, (
        "Para elevar o patamar do projeto profissionalmente, sugerimos as seguintes evoluções:\n\n"
        "• Notificações Push: Implementação de web-push para alertar o usuário sobre 'Furo de Reportagem' ou notícias urgentes.\n\n"
        "• Central de Estatísticas: Integração com APIs de futebol para exibir a tabela do campeonato, próximos jogos e artilharia em tempo real.\n\n"
        "• Busca Semântica: Sistema de busca para que o torcedor possa encontrar notícias passadas de jogadores específicos."
    ))

    # --- PAGE 5: ESTRATÉGIA DE MARKETING ---
    pdf.add_page()
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(eff_w, 10, '5. Estratégia de Marketing e Crescimento')
    pdf.ln(5)
    
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(eff_w, 8, (
        "O foco do marketing deve ser a 'Autoridade e Rapidez':\n\n"
        "• Automação de Redes Sociais: Criar robôs que postam automaticamente no X (Twitter) e threads no Instagram assim que uma notícia é gerada.\n\n"
        "• SEO Localizado: Otimizar o portal para termos de busca de alta intenção, como 'Escalação do Vasco hoje' ou 'Vasco ao vivo'.\n\n"
        "• Parcerias com Influenciadores: Engajamento com perfis menores que possuem público fiel, oferecendo o portal como ferramenta de consulta rápida."
    ))

    # --- PAGE 6: PLANO DE MONETIZAÇÃO ---
    pdf.add_page()
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(eff_w, 10, '6. Plano de Monetização')
    pdf.ln(5)
    
    pdf.set_x(margin)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(eff_w, 8, (
        "Existem diversas frentes para transformar o tráfego em receita:\n\n"
        "• Google AdSense: Implementação de banners nativos entre as notícias e no final dos artigos.\n\n"
        "• Marketing de Afiliados: Inclusão de links para camisas oficiais do Vasco (Amazon/Centauro) e parcerias com casas de apostas com bônus exclusivos para torcedores.\n\n"
        "• Publiposts Automáticos: Blogs patrocinados gerados pela IA sobre parceiros do clube ou serviços para o torcedor.\n\n"
        "• Conteúdo Premium/Club: Possibilidade de um 'acesso antecipado' ou sem anúncios para membros apoiadores."
    ))
    
    pdf.ln(20)
    pdf.set_x(margin)
    pdf.set_font('Arial', 'B', 14)
    pdf.multi_cell(eff_w, 10, 'Conclusão')
    pdf.ln(5)
    pdf.set_x(margin)
    pdf.set_font('Arial', 'I', 12)
    pdf.multi_cell(eff_w, 8, "O Vasco News está posicionado como uma solução tecnológica de ponta que une baixo custo operacional e alta entrega de valor. Com os ajustes estratégicos de marketing e monetização, o projeto tem potencial de se tornar o principal agregador de notícias da torcida vascaína.")

    output_path = 'Vasco_News_Estrategia.pdf'
    pdf.output(output_path)
    print(f"PDF gerado com sucesso em: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_pdf()
