import Link from "next/link";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { cache } from "react";
import MuseumGallery from "@/components/MuseumGallery";
import ExhibitList from "@/components/ExhibitList";
import SourceList from "@/components/SourceList";
import SpecimenCard from "@/components/SpecimenCard";
import KoleksiPanel from "@/components/KoleksiPanel";
import FacilityList from "@/components/FacilityList";
import ThreadOfRelation from "@/components/ThreadOfRelation";
import { chapterByIndex, ROMAN } from "@/lib/chapters";
import {
  attachMuseumDetail,
  mapMuseumRow,
  museumBySlugQuery,
  relatedCandidatesQuery,
} from "@/lib/queries";
import { pickRelated } from "@/lib/related";
import { runSelect, FusekiError } from "@/lib/sparql";
import { type MuseumDTO, type RelatedDTO } from "@/lib/types";

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

    const museum = await attachMuseumDetail(mapMuseumRow(rows[0]));

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

  if (result.status === "notfound") {
    return { title: "Museum tidak ditemukan — Museum Sumatera" };
  }

  if (result.status === "offline") {
    return { title: "Basis data tidak terjangkau — Museum Sumatera" };
  }

  return {
    title: `${result.museum.name} — Museum Sumatera`,
    description:
      result.museum.description ??
      `Catatan museum ${result.museum.name} dalam pameran digital Museum Sumatera.`,
  };
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
  const archiveNumber = chapter ? ROMAN[chapter.index - 1] ?? String(chapter.index) : undefined;

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
        <SpecimenCard museum={museum} archiveNumber={archiveNumber} />

        {(museum.collections?.length || museum.facilities?.length) ? (
          <div className="mt-12 grid gap-10 sm:grid-cols-2">
            <KoleksiPanel collections={museum.collections} />
            <FacilityList facilities={museum.facilities} />
          </div>
        ) : null}

        {museum.history.length > 0 && (
          <section className="mt-12">
            <h2 className="text-lg">Sejarah</h2>
            <div className="mt-3 space-y-3 text-[--ink-soft] leading-relaxed measure">
              {museum.history.map((paragraph, index) => (
                <p key={index} className="m-0">
                  {paragraph}
                </p>
              ))}
            </div>
          </section>
        )}

        {museum.exhibits.length > 0 && (
          <section className="mt-12">
            <h2 className="text-lg">Isi pameran</h2>
            <ExhibitList exhibits={museum.exhibits} />
          </section>
        )}

        <MuseumGallery images={museum.gallery} museumName={museum.name} />

        <ThreadOfRelation related={related} baseName={museum.name} />

        <SourceList sources={museum.sources} />
      </main>
    </div>
  );
}
