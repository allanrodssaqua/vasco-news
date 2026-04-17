import Header from "@/components/Header";
import WhatsAppButton from "@/components/WhatsAppButton";

export const metadata: Metadata = {
  title: "Vasco News | O Sentimento Não Pode Parar 💢",
  description: "Portal de notícias automatizado do Vasco da Gama em tempo real.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className="scroll-smooth">
      <body className="antialiased bg-black text-white min-h-screen flex flex-col">
        <Header />
        <main className="flex-grow">{children}</main>
        <WhatsAppButton />
      </body>
    </html>
  );
}
