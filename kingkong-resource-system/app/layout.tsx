import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '药师金刚资源位管理系统',
  description: '京东健康药师金刚资源位排期、提报、配置与询价管理平台',
  openGraph: {
    title: '药师金刚资源位管理系统',
    description: '排期 · 提报 · 配置 · 询价',
    images: [{ url: '/og.png', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: '药师金刚资源位管理系统',
    description: '排期 · 提报 · 配置 · 询价',
    images: ['/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
