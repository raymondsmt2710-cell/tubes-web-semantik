import Link from "next/link";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { cache } from "react";
import MuseumImage from "@/components/MuseumImage";
import ThreadOfRelation from "@/components/ThreadOfRelation";
import VerificationBadge from "@/components/VerificationBadge";
import { chapterByIndex } from "@/lib/chapters";
import {
  mapMuseumRow,
  museumBySlugQuery,
  relatedCandidatesQuery,
} from "@/lib/queries";
import { pickRelated } from "@/lib/related";
import { runSelect, FusekiError } from "@/lib/sparql";
import {
  eraLabel,
  themeLabels,
  yearLabel,
  type MuseumDTO,
  type RelatedDTO,
} from "@/lib/types";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ slug: string }>;
}

type LoadResult =
  | { status: "ok"; museum: MuseumDTO; related: RelatedDTO[] }
  | { status: "notfound" }
  | { status: "offline" };

/**
 * Satu pemuatan per permintaan: metadata dan badan halaman memakai hasil yang
 * sama, sehingga satu kunjungan tidak menembak Fuseki dua kali untuk data yang
 * identik.
 */
const loadMuseum = cache(async (slug: string): Promise<LoadResult> => {
  try {
    const rows = await runSelect(museumBySlugQuery(slug));
    if (rows.length === 0) return { status: "notfound" };

    const museum = mapMuseumRow(rows[0]);

    let related: RelatedDTO[] = [];
    try {
      const candidates = await runSelect(relatedCandidatesQuery(museum.slug));
      related = pickRelated(museum, candidates.map(mapMuseumRow));
    } catch {
      // Benang merah bersifat pelengkap; kegagalan query kedua tidak boleh
      // menjatuhkan seluruh halaman entri.
      related = [];
    }

    return { status: "ok", museum, related };
  } catch (error) {
    if (error instanceof FusekiError) return { status: "offline" };
    throw error;
  }
});

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const result = await loadMuseum(slug);

  if (result.status !== "ok") {
    return { title: "Museum tidak ditemukan — Museum Sumatera" };
  }

  return {
    title: `${result.museum.name} — Museum Sumatera`,
    description:
      result.museum.description ??
      `Catatan museum ${result.museum.name} dalam pameran digital Museum Sumatera.`,
  };
}

function MetaRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="grid grid-cols-[7.5rem_1fr] gap-3 py-2.5 border-b border-[--rule] text-sm">
      <dt className="label pt-0.5">{label}</dt>
      <dd className="m-0 text-[--ink]">{value}</dd>
    </div>
  );
}

export default async function MuseumPage({ params }: PageProps) {
  const { slug } = await params;
  const result = await loadMuseum(slug);

  if (result.status === "notfound") notFound();

  if (result.status === "offline") {
    return (
      <div className="min-h-screen paper-texture">
        <header className="mx-auto max-w-4xl px-5 pt-8">
          <Link href="/katalog" className="label">
            ← Katalog
          </Link>
        </header>
        <main className="mx-auto max-w-2xl px-5 pt-16 pb-20">
          <p className="label">Basis data tidak terjangkau</p>
          <h1 className="mt-3 text-2xl">Catatan museum belum dapat dimuat</h1>
          <p className="mt-3 text-sm text-[--ink-soft]">
            Halaman ini membaca data dari Apache Jena Fuseki, dan sambungan ke
            basis data sedang gagal. Coba muat ulang setelah basis data museum
            tersedia kembali.
          </p>
          <div className="mt-6 flex gap-3">
            <Link href="/katalog" className="btn">
              Kembali ke katalog
            </Link>
            <Link href="/" className="btn btn-ghost">
              Sampul
            </Link>
          </div>
        </main>
      </div>
    );
  }

  const { museum, related } = result;
  const chapter =
    museum.chapterIndex !== null ? chapterByIndex(museum.chapterIndex) : undefined;
  const themes = themeLabels(museum.themes);

  return (
    <div className="min-h-screen paper-texture">
      <header className="mx-auto max-w-4xl px-5 pt-8 flex items-center justify-between gap-4">
        {chapter ? (
          <Link href={`/jelajah/${chapter.index}`} className="label">
            ← {chapter.label} · {chapter.title}
          </Link>
        ) : (
          <Link href="/katalog" className="label">
            ← Katalog
          </Link>
        )}
        <nav className="flex gap-5 text-xs">
          <Link href="/katalog">Katalog</Link>
          <Link href="/tentang">Tentang</Link>
        </nav>
      </header>

      <main className="mx-auto max-w-4xl px-5 pt-10 pb-20">
        <p className="label">
          {[museum.city, museum.province].filter(Boolean).join(" · ") || "Lokasi tidak tercatat"}
        </p>
        <h1 className="mt-3 text-3xl sm:text-4xl max-w-2xl">{museum.name}</h1>

        <div className="mt-6 flex flex-wrap items-center gap-2">
          <VerificationBadge status={museum.verificationStatus} />
          {themes.map((theme) => (
            <span key={theme} className="chip">
              {theme}
            </span>
          ))}
        </div>

        <div className="mt-10 grid gap-x-10 gap-y-8 sm:grid-cols-[1.35fr_1fr]">
          <div>
            <MuseumImage src={museum.imageUrl} alt={`Museum ${museum.name}`} />

            <section className="mt-8">
              <h2 className="text-lg">Catatan koleksi</h2>
              <p className="mt-3 text-[--ink-soft] leading-relaxed measure">
                {museum.description ?? "Deskripsi museum ini belum tercatat."}
              </p>
            </section>

            {museum.officialUrl && (
              <p className="mt-5 text-sm">
                <a
                  href={museum.officialUrl}
                  target="_blank"
                  rel="noreferrer noopener"
                  className="underline decoration-[--accent]"
                >
                  Situs resmi museum ↗
                </a>
              </p>
            )}
          </div>

          <aside className="sm:border-l sm:border-[--rule] sm:pl-8">
            <h2 className="text-lg">Lembar data</h2>
            <dl className="mt-3 border-t border-[--rule]">
              <MetaRow label="Kota" value={museum.city ?? "Tidak tercatat"} />
              <MetaRow label="Provinsi" value={museum.province ?? "Tidak tercatat"} />
              <MetaRow label="Berdiri" value={yearLabel(museum.establishedYear)} />
              <MetaRow
                label="Tema"
                value={themes.length > 0 ? themes.join(", ") : "Tidak tercatat"}
              />
              <MetaRow label="Era" value={eraLabel(museum.era)} />
              <MetaRow label="Alamat" value={museum.address ?? "Tidak tercatat"} />
              <MetaRow
                label="Kunjungan"
                value={museum.admissionNote ?? "Belum ada catatan kunjungan."}
              />
              {chapter && (
                <MetaRow
                  label="Bab"
                  value={
                    <Link
                      href={`/jelajah/${chapter.index}`}
                      className="underline decoration-[--rule]"
                    >
                      {chapter.label} · {chapter.title}
                    </Link>
                  }
                />
              )}
            </dl>
            <p className="mt-4 text-xs text-[--ink-faint] measure">
              Data ini disusun untuk pembelajaran. Periksa jam buka dan koleksi
              pada sumber resmi sebelum berkunjung.
            </p>
          </aside>
        </div>

        <ThreadOfRelation related={related} baseName={museum.name} />
      </main>
    </div>
  );
}
