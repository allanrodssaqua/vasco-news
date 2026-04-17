import NewsCard from '@/components/NewsCard';
import newsData from '@/data/news.json';

export default function Home() {
  return (
    <div className="bg-[#000000] min-h-screen">
      <section className="max-w-7xl mx-auto px-6 py-12">
        {/* Grid de Notícias */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
          {newsData.map((news, index) => (
            <NewsCard 
              key={news.source_id || index}
              {...news}
            />
          ))}
        </div>

        {newsData.length === 0 && (
          <div className="flex flex-col items-center justify-center py-40 text-center">
            <h2 className="text-2xl font-black uppercase italic tracking-tighter opacity-10">Buscando Notícias...</h2>
          </div>
        )}

        {/* Footer Editorial Pro */}
        <footer className="mt-40 mb-20 flex flex-col items-center gap-10">
          {/* Selo CRVG */}
          <div className="h-14 w-14 border border-white/10 rounded-full flex items-center justify-center">
            <span className="text-[10px] font-black tracking-widest text-white/40">CRVG</span>
          </div>

          <div className="text-center space-y-2">
            <p className="text-[10px] uppercase tracking-[0.4em] text-white/20 font-black">
              © 2026 VASCONEWS • O SENTIMENTO NÃO PODE PARAR
            </p>
            <p className="text-[9px] uppercase tracking-[0.3em] text-white/10">
              Criado por Allan Rods • Tecnologia Gemini 3.1
            </p>
          </div>
        </footer>
      </section>
    </div>
  );
}
