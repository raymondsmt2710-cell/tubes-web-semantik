import Link from "next/link";
import type { Metadata } from "next";
import { CHAPTERS } from "@/lib/chapters";
import { ERAS, PROVINCES, THEMES, THEME_LABELS } from "@/lib/types";

export const metadata: Metadata = {
  title: "Tentang & Metode — Museum Sumatera",
  description:
    "Cara pameran digital Museum Sumatera disusun: data RDF, kueri SPARQL, alur tujuh bab, dan status verifikasi.",
};

export default function TentangPage() {
  return (
    <div className="min-h-screen paper-texture">
      <header className="mx-auto max-w-4xl px-5 pt-8 flex items-center justify-between">
        <Link href="/" className="label">
          ← Museum Sumatera
        </Link>
        <nav className="flex gap-5 text-xs">
          <Link href="/katalog">Katalog</Link>
          <Link href="/tentang" aria-current="page" className="underline">
            Tentang
          </Link>
        </nav>
      </header>

      <main className="mx-auto max-w-3xl px-5 pt-12 pb-20">
        <p className="label">Tentang pameran</p>
        <h1 className="display mt-3 text-3xl sm:text-4xl">
          Arsip yang dibaca sebagai perjalanan
        </h1>
        <p className="prose-lede mt-6 measure">
          Situs ini bukan katalog datar. Museum-museum di Pulau Sumatera disusun
          sebagai tujuh bab perjalanan dari Aceh ke Lampung, lalu dihubungkan
          kembali lewat tema, kota, era, dan kedekatan bab. Semua hubungan itu
          dihitung dari data, bukan ditulis tangan di halaman.
        </p>

        <hr className="rule mt-10" />

        <section className="mt-10">
          <h2 className="text-xl">Bagaimana data disimpan</h2>
          <div className="mt-4 space-y-3 text-sm text-[--ink-soft] measure">
            <p>
              Data museum disimpan sebagai RDF — bukan tabel biasa. Setiap museum
              adalah sebuah subjek dengan properti seperti provinsi, kota, tema,
              era, tahun berdiri, dan bab. Bentuk ini membuat relasi antarmuseum
              bisa ditanyakan langsung, tanpa menduplikasi daftar di kode.
            </p>
            <p>
              Basis data yang dipakai adalah Apache Jena Fuseki. Aplikasi ini
              hanya mengirim kueri SPARQL; penyaringan provinsi, tema, era, dan
              tahun dilakukan di sisi basis data, bukan dengan menyaring array di
              browser. Halaman-halaman Next.js memakai hasil kueri yang sama
              dengan API publiknya.
            </p>
            <p>
              Skrip <code className="font-mono text-xs">npm run generate:rdf</code>{" "}
              mengubah berkas sumber <code className="font-mono text-xs">data/museums.json</code>{" "}
              menjadi RDF/XML, lalu <code className="font-mono text-xs">npm run upload:fuseki</code>{" "}
              mengunggahnya ke Fuseki bila endpoint di <code className="font-mono text-xs">.env</code>{" "}
              sudah diisi.
            </p>
          </div>
        </section>

        <section className="mt-10">
          <h2 className="text-xl">Cakupan</h2>
          <dl className="mt-4 grid grid-cols-2 gap-x-6 gap-y-3 text-sm sm:grid-cols-4">
            <div>
              <dt className="label">Bab</dt>
              <dd className="font-serif text-2xl">{CHAPTERS.length}</dd>
            </div>
            <div>
              <dt className="label">Provinsi</dt>
              <dd className="font-serif text-2xl">{PROVINCES.length}</dd>
            </div>
            <div>
              <dt className="label">Tema</dt>
              <dd className="font-serif text-2xl">{THEMES.length}</dd>
            </div>
            <div>
              <dt className="label">Era</dt>
              <dd className="font-serif text-2xl">{ERAS.length}</dd>
            </div>
          </dl>
          <p className="mt-4 text-sm text-[--ink-soft] measure">
            Tema yang dipakai: {THEMES.map((theme) => THEME_LABELS[theme]).join(", ")}.
          </p>
        </section>

        <section className="mt-10">
          <h2 className="text-xl">Benang merah</h2>
          <p className="mt-3 text-sm text-[--ink-soft] measure">
            Di halaman setiap museum ada bagian &ldquo;benang merah&rdquo;. Museum lain
            dipilih bila berbagi tema (+3 per tema), berada di kota yang sama (+2),
            berada di era yang sama (+1), atau berada di bab yang bersebelahan
            (+1). Kandidat dengan skor nol tidak ditampilkan, dan urutan seri
            dipecah berdasarkan nama agar hasilnya tetap sama setiap kali dibuka.
          </p>
        </section>

        <section className="mt-10">
          <h2 className="text-xl">Status verifikasi</h2>
          <p className="mt-3 text-sm text-[--ink-soft] measure">
            Seluruh entri saat ini ditandai{" "}
            <span className="chip">Perlu verifikasi</span>. Artinya nama, alamat,
            tahun berdiri, dan catatan kunjungan disusun untuk keperluan
            pembelajaran dan belum diperiksa ulang terhadap sumber resmi. Lencana
            pada setiap halaman museum menunjukkan status ini secara terbuka.
            Jangan memakai data di sini sebagai rujukan perjalanan tanpa
            memeriksanya kembali.
          </p>
        </section>

        <section className="mt-10">
          <h2 className="text-xl">Alur bab</h2>
          <ol className="mt-4 border-t border-[--rule]">
            {CHAPTERS.map((chapter) => (
              <li key={chapter.index} className="border-b border-[--rule] py-3">
                <Link
                  href={`/jelajah/${chapter.index}`}
                  className="flex items-baseline gap-4 group"
                >
                  <span className="label w-14 shrink-0">{chapter.label}</span>
                  <span className="flex-1">
                    <span className="font-serif text-base group-hover:underline block">
                      {chapter.title}
                    </span>
                    <span className="text-xs text-[--ink-soft]">
                      {chapter.provinces.join(" · ")}
                    </span>
                  </span>
                  <span aria-hidden className="text-[--ink-faint]">
                    →
                  </span>
                </Link>
              </li>
            ))}
          </ol>
        </section>

        <div className="mt-12 flex flex-wrap gap-3">
          <Link href="/katalog" className="btn">
            Telusuri katalog
          </Link>
          <Link href="/" className="btn btn-ghost">
            Kembali ke sampul
          </Link>
        </div>
      </main>
    </div>
  );
}
