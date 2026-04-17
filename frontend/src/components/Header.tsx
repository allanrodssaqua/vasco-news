import Link from 'next/link';
import React from 'react';

export default function Header() {
  return (
    <header className="border-b border-white/5 bg-black/50 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <Link href="/" className="group flex flex-col">
          <div className="flex items-center gap-3 mb-2">
            <span className="h-0.5 w-12 bg-[#c4121a] group-hover:w-16 transition-all duration-300" />
            <p className="text-[12px] uppercase tracking-[0.4em] text-white/40 font-black">
              Agregador Oficial
            </p>
          </div>
          <h1 className="text-5xl md:text-7xl font-black tracking-tighter uppercase italic">
            Vasco<span className="text-[#c4121a]">News</span>
          </h1>
        </Link>
        
        <div className="text-right hidden md:block">
          <p className="text-sm font-bold opacity-30 uppercase tracking-widest">
            {new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: 'long' })}
          </p>
        </div>
      </div>
    </header>
  );
}
