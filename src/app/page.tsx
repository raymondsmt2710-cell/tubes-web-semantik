import Link from "next/link";
import ChapterList from "@/components/ChapterList";
import SearchBox from "@/components/SearchBox";
import { runSelect } from "@/lib/sparql";
import { chaptersQuery } from "@/lib/queries";

export const dynamic = "force-dynamic";

async function loadCounts(): Promise<Map<number, number> | null> {
  try {
    const rows = await runSelect(chaptersQuery());
    const counts = new Map<number, number>();
    for (const row of rows) {
      const index = Number(row.chapterIndex?.value);
      const count = Number(row.museumCount?.value);
      if (Number.isFinite(index)) counts.set(index, Number.isFinite(count) ? count : 0);
    }
    return counts;
  } catch {
    return null;
  }
}

export default async function Home() {
  const counts = await loadCounts();

  return (
    <div className="min-h-screen paper-texture">
      <header className="mx-auto max-w-5xl px-5 pt-8 flex items-center justify-between">
        <span className="label">Museum Sumatera</span>
        <nav className="flex gap-5 text-xs">
          <Link href="/katalog">Katalog</Link>
          <Link href="/tentang">Tentang</Link>
        </nav>
      </header>

      <main className="mx-auto max-w-5xl px-5 pt-14 pb-20">
        <p className="label">Pameran digital · Sepuluh provinsi</p>
        <h1 className="display mt-4 max-w-3xl">
          Perjalanan dari Aceh ke Lampung
        </h1>
        <p className="prose-lede mt-6 measure">
          Pulau Sumatera menyimpan ingatan dalam bentuk yang berbeda-beda: naskah
          di Banda Aceh, rumah adat di tepi Danau Toba, istana Melayu di Siak,
          lokomotif tambang di Sawahlunto, dan arca Sriwijaya di tepi Musi. Tujuh
          bab berikut menyusunnya sebagai satu perjalanan, dari pelabuhan barat
          sampai gerbang Selat Sunda.
        </p>

        <div className="mt-10 max-w-xl">
          <SearchBox />
          <p className="text-xs text-[--ink-soft] mt-2">
            Bisa juga langsung mencari: “etnografi”, “Palembang”, “timah”.
          </p>
        </div>

        <section className="mt-14">
          <div className="flex items-baseline justify-between mb-3">
            <h2 className="text-xl">Alur pameran</h2>
            <Link href="/katalog" className="text-xs underline">
              Lihat katalog lengkap
            </Link>
          </div>

          <ChapterList counts={counts} />

          {counts === null && (
            <p className="mt-4 text-sm border border-[--rule] bg-[--paper-2] px-4 py-3 rounded-sm">
              Basis data museum sedang tidak dapat dihubungi. Alur bab tetap bisa
              dibaca, tetapi daftar museum belum dapat dimuat.
            </p>
          )}
        </section>

        <section className="mt-16 grid gap-8 sm:grid-cols-3">
          <div>
            <p className="label">Metode</p>
            <p className="mt-2 text-sm text-[--ink-soft]">
              Data museum disimpan sebagai RDF di Apache Jena Fuseki dan dibaca
              lewat SPARQL. Relasi antarmuseum dipakai untuk menyusun benang merah,
              bukan dikarang di halaman.
            </p>
          </div>
          <div>
            <p className="label">Cakupan</p>
            <p className="mt-2 text-sm text-[--ink-soft]">
              Tujuh bab, sepuluh provinsi, enam tema koleksi. Seluruh data masih
              dalam tahap verifikasi.
            </p>
          </div>
          <div>
            <p className="label">Cara membaca</p>
            <p className="mt-2 text-sm text-[--ink-soft]">
              Mulai dari Bab I lalu ikuti tautan bab berikutnya, atau lompat ke
              katalog bila Anda sudah tahu apa yang dicari.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}
