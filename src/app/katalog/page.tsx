import Link from "next/link";
import type { Metadata } from "next";
import { Suspense } from "react";
import CatalogView from "@/components/CatalogView";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Katalog — Museum Sumatera",
  description:
    "Telusuri seluruh museum di Pulau Sumatera dengan penyaringan provinsi, tema, era, dan tahun, langsung dari basis data SPARQL.",
};

export default function KatalogPage() {
  return (
    <div className="min-h-screen paper-texture">
      <header className="mx-auto max-w-4xl px-5 pt-8 flex items-center justify-between">
        <Link href="/" className="label">
          ← Museum Sumatera
        </Link>
        <nav className="flex gap-5 text-xs">
          <Link href="/katalog" aria-current="page" className="underline">
            Katalog
          </Link>
          <Link href="/tentang">Tentang</Link>
        </nav>
      </header>

      <main className="mx-auto max-w-4xl px-5 pt-12 pb-20">
        <p className="label">Katalog</p>
        <h1 className="display mt-3 text-3xl sm:text-4xl">
          Seluruh museum, satu arsip
        </h1>
        <p className="prose-lede mt-5 measure">
          Kalau alur bab membawa Anda dari Aceh ke Lampung, katalog ini
          membaliknya: semua entri terbuka sekaligus. Setiap penyaring dikirim
          sebagai kueri ke basis data, jadi hasilnya selalu berasal dari data —
          bukan dari daftar yang disaring di layar.
        </p>

        <Suspense
          fallback={
            <p className="mt-10 text-sm text-[--ink-soft]">Memuat katalog…</p>
          }
        >
          <CatalogView />
        </Suspense>
      </main>
    </div>
  );
}
