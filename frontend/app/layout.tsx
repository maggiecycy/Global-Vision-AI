import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Navbar from "@/components/common/Navbar";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Global Vision AI",
  description: "Personalized multilingual news digest system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // suppressHydrationWarning 解决浏览器插件注入导致的红屏报错
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-zinc-50 pt-16`}
      >
        {/* 全局导航栏 */}
        <Navbar />
        
        {/* 各个页面的内容会在这里渲染 */}
        <main className="max-w-6xl mx-auto min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}