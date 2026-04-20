import Link from 'next/link';
import React from 'react';
import NewsImage from './NewsImage';

interface NewsCardProps {
  title: string;
  subtitle: string;
  date: string;
  source_url: string;
  source_id: string;
}

export default function NewsCard({ title, subtitle, date, source_url, source_id }: NewsCardProps) {
  const isYoutube = !source_url.includes('globo.com') && 
                    !source_url.includes('lance.com.br') && 
                    !source_url.includes('espn.com.br');

  const sourceName = isYoutube ? "VASCO TV / YOUTUBE" : "PORTAL / RSS";

  const formattedDate = new Date(date).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long'
  }).toUpperCase();

  return (
    <Link 
      href={`/noticia/${source_id}`} 
      className="news-card-hover group editorial-card flex flex-col h-full rounded-lg"
    >
      {/* Thumbnail */}
      <NewsImage 
        source_id={source_id}
        source_url={source_url}
        title={title}
        className="aspect-video"
      />

      {/* Content Body */}
      <div className="p-7 flex flex-col flex-grow">
        {/* Accent Bar + Date */}
        <div className="flex flex-col gap-2 mb-4">
          <div className="h-[2px] w-6 bg-[#c4121a]" />
          <time className="text-[10px] font-black tracking-widest text-white/40 uppercase">
            {formattedDate}
          </time>
        </div>

        {/* Title */}
        <h3 className="text-[22px] md:text-2xl font-bold leading-[1.15] tracking-tight mb-4 group-hover:text-white/90 transition-colors">
          {title}
        </h3>

        {/* Subtitle / Excerpt */}
        <p className="text-sm font-light leading-relaxed text-white/40 line-clamp-2 mb-8">
          {subtitle}
        </p>

        {/* Card Footer (Static in reference) */}
        <div className="mt-auto pt-6 border-t border-white/[0.03] flex items-center justify-between">
          <span className="text-[9px] font-black tracking-[0.2em] text-white/20 uppercase">
            {sourceName}
          </span>
          <svg className="w-4 h-4 text-white/10 group-hover:text-white/40 group-hover:translate-x-1 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </div>
      </div>
    </Link>
  );
}
