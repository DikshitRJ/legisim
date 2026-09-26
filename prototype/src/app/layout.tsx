import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LEGISIM — Legislative Simulation Portal",
  description: "AI-powered policy impact simulation for the Government of India",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-canvas text-text-body font-sans min-h-screen antialiased">
        {/* Indian Tricolor Top Bar */}
        <div className="fixed top-0 left-0 right-0 h-[3px] z-[60] flex w-full">
          <div className="h-full flex-1 bg-saffron" />
          <div className="h-full flex-1 bg-white/90" />
          <div className="h-full flex-1 bg-india-green" />
        </div>
        <div className="pt-[3px]">
          {children}
        </div>
      </body>
    </html>
  );
}
