"use client";

import Link from 'next/link';
import React from 'react';

interface NewsCardProps {
  title: string;
  subtitle: string;
  date: string;
  source_url: string;
  source_id: string;
}

export default function NewsCard({ title, subtitle, date, source_url, source_id }: NewsCardProps) {
  // Gera thumbnail do YouTube ou placeholder para RSS
  const isYoutube = !source_url.includes('globo.com') && !source_url.includes('lance.com.br');
  const thumbnailUrl = isYoutube 
    ? `https://img.youtube.com/vi/${source_id}/maxresdefault.jpg`
    : `https://raw.githubusercontent.com/lucasrods/antigravity-assets/main/vasco-placeholder.jpg`; // Placeholder genérico

  return (
    <Link 
      href={`/noticia/${source_id}`} 
      className="news-card-hover group block bg-[#0a0a0a] border border-[#1a1a1a] rounded-xl overflow-hidden cursor-pointer transition-all duration-300 hover:border-white/20"
    >
      {/* Container da Imagem com Zoom */}
      <div className="relative h-48 w-full overflow-hidden">
        <img 
          src={thumbnailUrl} 
          alt={title}
          className="smooth-scale h-full w-full object-cover grayscale-[0.3] group-hover:grayscale-0 transition-all duration-500"
          onError={(e) => {
            (e.target as HTMLImageElement).src = "https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=1000&auto=format&fit=crop"; 
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
      </div>

      {/* Conteúdo */}
      <div className="p-5 flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <span className="h-1 w-8 bg-[#c4121a]" />
          <p className="text-[10px] uppercase tracking-[0.2em] text-white/50 font-bold">
            {new Date(date).toLocaleDateString('pt-BR', { day: '2-digit', month: 'long' })}
          </p>
        </div>
        
        <h2 className="text-xl font-bold leading-tight group-hover:text-[#c4121a] transition-colors duration-300">
          {title}
        </h2>
        
        <p className="text-sm text-white/60 line-clamp-2 font-light leading-relaxed">
          {subtitle}
        </p>

        <div className="mt-2 pt-4 border-t border-white/5 flex justify-between items-center">
          <span className="text-[10px] uppercase tracking-widest font-bold text-white/30">
            {isYoutube ? 'Vasco TV / YouTube' : 'Portal de Notícias'}
          </span>
          <svg className="w-4 h-4 text-white/20 group-hover:text-white transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="arrow-narrow-right" />
            <path d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </div>
      </div>
    </Link>
  );
}
