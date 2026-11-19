import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import ChapterNav from "@/components/ChapterNav";
import MuseumEntry from "@/components/MuseumEntry";
import { chapterByIndex, CHAPTERS } from "@/lib/chapters";
import { museumsByChapterQuery, mapMuseumRow } from "@/lib/queries";
import { runSelect } from "@/lib/sparql";

export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{ chapter: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { chapter } = await params;
  const index = Number(chapter);
  const definition = Number.isInteger(index) ? chapterByIndex(index) : undefined;
  return {
    title: definition
      ? `${definition.label} — ${definition.title}`
      : "Bab tidak ditemukan",
  };
}

export default async function ChapterPage({ params }: PageProps) {
  const { chapter } = await params;
  const index = Number(chapter);

  if (!Number.isInteger(index) || index < 1 || index > CHAPTERS.length) {
    notFound();
  }

  const definition = chapterByIndex(index);
  if (!definition) notFound();

  let museums: Awaited<ReturnType<typeof load>> | null = null;
  try {
    museums = await load(index);
  } catch {
    museums = null;
  }

  return (
    <div className="min-h-screen paper-texture">
      <header className="mx-auto max-w-4xl px-5 pt-8 flex items-center justify-between">
        <Link href="/" className="label">
          ← Museum Sumatera
        </Link>
        <nav className="flex gap-5 text-xs">
          {CHAPTERS.map((item) => (
            <Link
              key={item.index}
              href={`/jelajah/${item.index}`}
              className={
                item.index === index
                  ? "underline decoration-[--accent] decoration-2 underline-offset-4"
                  : "text-[--ink-soft]"
              }
              aria-current={item.index === index ? "page" : undefined}
            >
              {item.index}
            </Link>
          ))}
        </nav>
      </header>

      <main className="mx-auto max-w-4xl px-5 pt-12 pb-20">
        <p className="label">
          {definition.label} · {definition.provinces.join(" · ")}
        </p>
        <h1 className="mt-3 text-3xl sm:text-4xl max-w-2xl">{definition.title}</h1>
        <p className="prose-lede mt-5 measure">{definition.intro}</p>

        <section className="mt-12">
          <div className="flex items-baseline justify-between mb-2">
            <h2 className="text-lg">
              {museums ? `${museums.length} museum dalam bab ini` : "Daftar museum"}
            </h2>
            <Link href="/katalog" className="text-xs underline">
              Katalog lengkap
            </Link>
          </div>

          {museums === null && (
            <p className="text-sm border border-[--rule] bg-[--paper-2] px-4 py-3 rounded-sm">
              Basis data museum sedang tidak dapat dihubungi, jadi daftar museum
              belum bisa ditampilkan. Narasi bab tetap tersedia.
            </p>
          )}

          {museums !== null && museums.length === 0 && (
            <p className="text-sm text-[--ink-soft]">
              Belum ada museum yang tercatat pada bab ini.
            </p>
          )}

          {museums !== null && museums.length > 0 && (
            <div className="border-t border-[--rule]">
              {museums.map((museum, position) => (
                <MuseumEntry key={museum.slug} museum={museum} index={position + 1} />
              ))}
            </div>
          )}
        </section>

        <ChapterNav current={index} />
      </main>
    </div>
  );
}

async function load(index: number) {
  const rows = await runSelect(museumsByChapterQuery(index));
  return rows.map(mapMuseumRow);
}
