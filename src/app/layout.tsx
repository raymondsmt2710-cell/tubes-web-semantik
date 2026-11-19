import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Museum Sumatera — Pameran Digital",
  description:
    "Jelajahi museum di Pulau Sumatera, dari Aceh hingga Lampung, lewat alur pameran dan pencarian data berbasis RDF.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="id">
      <body>
        {children}
        <footer className="rule mt-16">
          <div className="mx-auto max-w-5xl px-5 py-10 text-sm text-[--ink-soft]">
            <p className="measure">
              Data museum disusun untuk keperluan pembelajaran dan belum
              seluruhnya terverifikasi. Selalu periksa jam buka dan koleksi pada
              sumber resmi sebelum berkunjung.
            </p>
            <nav className="mt-4 flex flex-wrap gap-x-5 gap-y-2 text-xs">
              <Link href="/">Sampul</Link>
              <Link href="/katalog">Katalog</Link>
              <Link href="/tentang">Tentang &amp; Metode</Link>
            </nav>
            <p className="label mt-6">Museum Sumatera · Pameran Digital</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
