import newsData from '@/data/news.json';
import { notFound } from 'next/navigation';

interface Props {
  params: Promise<{ id: string }>;
}

export async function generateStaticParams() {
  return newsData.map((news) => ({
    id: news.source_id,
  }));
}

export default async function NoticiaPage({ params }: Props) {
  const { id } = await params;
  const noticia = newsData.find((n) => n.source_id === id);

  if (!noticia) {
    notFound();
  }

  const isYoutube = !noticia.source_url.includes('globo.com') && !noticia.source_url.includes('lance.com.br');
  const thumbnailUrl = isYoutube 
    ? `https://img.youtube.com/vi/${noticia.source_id}/maxresdefault.jpg`
    : `https://raw.githubusercontent.com/lucasrods/antigravity-assets/main/vasco-placeholder.jpg`;

  return (
    <article className="min-h-screen bg-[#000000] text-white selection:bg-[#c4121a] selection:text-white pb-20">
      {/* Hero Header com Thumbnail */}
      <div className="relative w-full h-[50vh] md:h-[70vh] overflow-hidden">
        {/* Botão Voltar Mobile-First */}
        <div className="absolute top-6 left-6 z-20">
          <Link 
            href="/" 
            className="flex items-center gap-2 px-6 py-3 bg-black/50 backdrop-blur-md border border-white/10 rounded-full text-xs font-bold uppercase tracking-widest hover:bg-white hover:text-black transition-all duration-300 min-h-[44px]"
          >
            ← Voltar para o Início
          </Link>
        </div>
        <img 
          src={thumbnailUrl} 
          alt={noticia.title}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent" />
      </div>

      {/* Conteúdo da Matéria */}
      <div className="max-w-4xl mx-auto px-6 -mt-32 relative z-10">
        <header className="mb-12">
          <div className="flex items-center gap-3 mb-6">
            <span className="h-0.5 w-12 bg-[#c4121a]" />
            <p className="text-[12px] uppercase tracking-[0.4em] text-white/60 font-black">
              {new Date(noticia.date).toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })}
            </p>
          </div>
          
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter leading-none mb-6">
            {noticia.title}
          </h1>
          
          <p className="text-xl md:text-2xl text-white/50 font-light leading-relaxed italic">
            {noticia.subtitle}
          </p>
        </header>

        <section className="prose prose-invert prose-lg max-w-none">
          <div className="text-white/80 leading-loose space-y-8 text-lg md:text-xl font-light px-0 md:px-0">
            {noticia.content.split('\n').map((paragraph, idx) => (
              <p key={idx}>{paragraph}</p>
            ))}
          </div>
        </section>

        {/* Rodapé da Matéria */}
        <footer className="mt-20 pt-10 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className="h-10 w-10 border border-[#c4121a] rounded-full flex items-center justify-center">
              <span className="text-[10px] font-bold">AR</span>
            </div>
            <div>
              <p className="text-xs uppercase tracking-widest font-bold">ALLAN RODS | Curadoria Automática</p>
              <p className="text-[10px] text-white/30 uppercase">Inteligência Artificial & Jornalismo</p>
            </div>
          </div>
          
          <a 
            href={noticia.source_url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="px-8 py-3 bg-white text-black text-xs font-bold uppercase tracking-widest hover:bg-[#c4121a] hover:text-white transition-all duration-300 rounded-sm"
          >
            Ver Fonte Original
          </a>
        </footer>
      </div>
    </article>
  );
}
