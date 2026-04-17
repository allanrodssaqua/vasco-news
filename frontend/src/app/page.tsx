import NewsCard from '@/components/NewsCard';
import newsData from '@/data/news.json';

export default function Home() {
  return (
    <main className="min-h-screen bg-[#000000] text-white selection:bg-[#c4121a] selection:text-white">
      {/* Header Editorial */}
      <header className="border-b border-white/5 bg-black/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="flex flex-col">
            <div className="flex items-center gap-3 mb-2">
              <span className="h-0.5 w-12 bg-[#c4121a]" />
              <p className="text-[12px] uppercase tracking-[0.4em] text-white/40 font-black">
                Agregador Oficial
              </p>
            </div>
            <h1 className="text-5xl md:text-7xl font-black tracking-tighter uppercase italic">
              Vasco<span className="text-[#c4121a]">News</span>
            </h1>
          </div>
          
          <div className="text-right hidden md:block">
            <p className="text-sm font-bold opacity-30 uppercase tracking-widest">
              {new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: 'long' })}
            </p>
          </div>
        </div>
      </header>

      {/* Grid de Notícias */}
      <section className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {newsData.map((news, index) => (
            <NewsCard 
              key={news.source_id || index}
              {...news}
            />
          ))}
        </div>

        {newsData.length === 0 && (
          <div className="flex flex-col items-center justify-center py-32 text-center opacity-20">
            <h2 className="text-2xl font-bold uppercase italic">Buscando notícias no front...</h2>
            <p className="text-sm tracking-widest mt-2 uppercase">Aguarde a próxima atualização automática</p>
          </div>
        )}
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-12">
        <div className="max-w-7xl mx-auto px-6 flex flex-col items-center gap-4 text-center">
          <div className="h-10 w-10 border border-white/10 rounded-full flex items-center justify-center mb-4">
            <span className="text-[10px] font-bold">CRVG</span>
          </div>
          <p className="text-[10px] uppercase tracking-[0.3em] text-white/30 font-bold">
            © 2026 VascoNews • O Sentimento Não Pode Parar
          </p>
        </div>
      </footer>
    </main>
  );
}
