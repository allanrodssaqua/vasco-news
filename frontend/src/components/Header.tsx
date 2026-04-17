import Link from 'next/link';
import React from 'react';

export default function Header() {
  const currentDate = new Date().toLocaleDateString('pt-BR', { 
    weekday: 'long', 
    day: '2-digit', 
    month: 'long' 
  }).toUpperCase();

  return (
    <header className="bg-[#000000] border-b border-white/[0.03] pt-12 pb-16">
      <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row md:items-end justify-between items-start gap-8">
        <Link href="/" className="group inline-block">
          {/* Top Line Branding */}
          <div className="flex items-center gap-3 mb-1">
            <span className="h-[1.5px] w-8 bg-[#c4121a]" />
            <p className="text-[10px] md:text-[11px] uppercase tracking-[0.6em] text-white/40 font-bold">
              Agregador Oficial
            </p>
          </div>
          
          {/* Main Logo */}
          <h1 className="text-6xl md:text-8xl vasco-news-title flex items-baseline">
            VASCO<span className="text-[#c4121a]">NEWS</span>
          </h1>
        </Link>
        
        {/* Date Display */}
        <div className="text-right">
          <p className="text-[11px] md:text-xs font-black text-white/20 uppercase tracking-[0.3em]">
            {currentDate}
          </p>
        </div>
      </div>
    </header>
  );
}
