"use client";

import React from 'react';

interface NewsImageProps {
  source_id: string;
  source_url: string;
  title: string;
  className?: string;
  priority?: boolean;
}

export default function NewsImage({ source_id, source_url, title, className = "", priority = false }: NewsImageProps) {
  const [imgStatus, setImgStatus] = React.useState<'loading' | 'success' | 'error'>('loading');
  const [retryWithHq, setRetryWithHq] = React.useState(false);

  const isYoutube = !source_url.includes('globo.com') && 
                    !source_url.includes('lance.com.br') && 
                    !source_url.includes('espn.com.br');

  const customThumbnail = `/thumbnails/${source_id}.png`;

  const getThumbnailUrl = () => {
    if (isYoutube) {
      if (retryWithHq) return `https://img.youtube.com/vi/${source_id}/hqdefault.jpg`;
      return `https://img.youtube.com/vi/${source_id}/maxresdefault.jpg`;
    }
    return `/placeholder.png`;
  };

  return (
    <div className={`relative overflow-hidden bg-[#0a0a0a] ${className}`}>
      {imgStatus !== 'error' ? (
        <>
          <img 
            src={customThumbnail}
            alt=""
            className={`absolute inset-0 w-full h-full object-cover z-10 transition-opacity duration-500 ${imgStatus === 'success' ? 'opacity-100' : 'opacity-0'}`}
            onError={(e) => {
              (e.target as HTMLImageElement).style.display = 'none';
            }}
          />
          <img 
            src={getThumbnailUrl()} 
            alt={title}
            className={`w-full h-full object-cover transition-transform duration-700 ${imgStatus === 'success' ? 'scale-100' : 'scale-110'}`}
            onLoad={() => setImgStatus('success')}
            loading={priority ? 'eager' : 'lazy'}
            onError={() => {
              if (isYoutube && !retryWithHq) {
                setRetryWithHq(true);
              } else {
                setImgStatus('error');
              }
            }}
          />
        </>
      ) : (
        <div className="w-full h-full flex flex-col items-center justify-center p-6 text-center bg-gradient-to-br from-[#0c0c0c] to-[#151515] relative overflow-hidden">
           <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.03] scale-[2.5]">
             <svg viewBox="0 0 100 100" className="w-40 h-40 fill-white">
               <path d="M50 0L65 35L100 50L65 65L50 100L35 65L0 50L35 35Z" />
             </svg>
           </div>
           
           <div className="relative z-10 space-y-3">
              <div className="h-1 w-12 bg-[#c4121a] mx-auto mb-4" />
              <h4 className="text-lg font-black leading-tight uppercase italic tracking-tighter line-clamp-3 px-4">
                {title}
              </h4>
              <div className="pt-2">
                <span className="text-[8px] font-black tracking-[0.4em] text-[#c4121a] uppercase bg-[#c4121a]/5 px-2 py-1 rounded-full">
                  Curadoria Esportiva
                </span>
              </div>
           </div>
        </div>
      )}
    </div>
  );
}
