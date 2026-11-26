import Link from "next/link";
import type { Metadata } from "next";
import { AskPanel } from "@/components/AskPanel";

export const metadata: Metadata = {
  title: "Tanya — Museum Sumatera",
  description:
    "Ajukan pertanyaan bahasa Indonesia tentang museum di Pulau Sumatera. Jawaban disusun dari graf RDF, lengkap dengan query SPARQL dan sumbernya.",
};

export default function TanyaPage() {
  return (
    <div className="min-h-screen paper-texture">
      <header className="mx-auto max-w-4xl px-5 pt-8 flex items-center justify-between">
        <Link href="/" className="label">
          ← Museum Sumatera
        </Link>
        <nav className="flex gap-5 text-xs">
          <Link href="/katalog">Katalog</Link>
          <Link href="/tanya" aria-current="page" className="underline">
            Tanya
          </Link>
          <Link href="/tentang">Tentang</Link>
        </nav>
      </header>

      <main className="mx-auto max-w-3xl px-5 pt-12 pb-20">
        <p className="label">Tanya jawab berbasis graf</p>
        <h1 className="display mt-3 text-3xl sm:text-4xl">
          Bertanya kepada arsip, bukan menebak
        </h1>
        <p className="prose-lede mt-6 measure">
          Pertanyaan Anda diterjemahkan menjadi kueri SPARQL, diperiksa lebih dulu,
          lalu dijalankan pada graf museum. Jawaban hanya disusun dari data yang
          benar-benar keluar dari kueri itu — bila graf tidak memuat jawabannya,
          sistem berkata tidak ditemukan, bukan mengarang.
        </p>

        <hr className="rule mt-10" />

        <AskPanel />

        <section className="mt-14 text-sm text-[--ink-soft] measure">
          <h2 className="text-xl text-[--ink]">Bagaimana jawabannya dijaga</h2>
          <ol className="mt-4 list-decimal space-y-2 pl-5">
            <li>
              <strong>Skema dari graf.</strong> Hanya nama kelas dan properti yang ada
              di data yang boleh dipakai. Properti karangan ditolak.
            </li>
            <li>
              <strong>Guard sebelum eksekusi.</strong> Kueri wajib berbentuk{" "}
              <code className="font-mono text-xs">SELECT</code>, wajib memakai{" "}
              <code className="font-mono text-xs">LIMIT</code> kecil, dan hanya boleh
              menyebut IRI yang dikenal.
            </li>
            <li>
              <strong>Jawaban dari data.</strong> Hasil kosong dijawab &ldquo;tidak
              ditemukan di graf&rdquo; tanpa diserahkan ke model bahasa.
            </li>
            <li>
              <strong>Sumber ditempel kode.</strong> IRI sumber diambil dari hasil
              kueri, bukan dikarang oleh model.
            </li>
          </ol>
          <p className="mt-4">
            Guard memeriksa bentuk kueri, bukan hak akses pengguna. Otorisasi
            dilakukan terpisah di server.
          </p>
        </section>
      </main>
    </div>
  );
}
