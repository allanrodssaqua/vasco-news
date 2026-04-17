import NewsCard from '@/components/NewsCard';
import newsData from '@/data/news.json';

export default function Home() {
  return (
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

      {/* Footer Simples */}
      <div className="mt-32 pt-12 border-t border-white/5 flex flex-col items-center gap-4 text-center">
        <div className="h-10 w-10 border border-white/10 rounded-full flex items-center justify-center mb-4">
          <span className="text-[10px] font-bold">AR</span>
        </div>
        <p className="text-[10px] uppercase tracking-[0.3em] text-white/30 font-bold">
          Criado por Allan Rods • O Sentimento Não Pode Parar
        </p>
        <p className="text-[9px] uppercase tracking-[0.2em] text-white/10">
          © 2026 VascoNews • Tecnologia Gemini 3.1
        </p>
      </div>
    </section>
  );
}
