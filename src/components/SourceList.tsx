import type { SourceRef } from "@/lib/types";

interface SourceListProps {
  sources: SourceRef[];
}

/**
 * Sumber acuan supaya pembaca bisa memeriksa sendiri catatan yang ditampilkan.
 * Tautan dibuka di tab baru dan memakai rel=noreferrer.
 */
export default function SourceList({ sources }: SourceListProps) {
  if (sources.length === 0) return null;

  return (
    <section className="mt-12 border-t border-[--rule] pt-5">
      <h2 className="label">Sumber catatan</h2>
      <ul className="mt-3 m-0 p-0 list-none space-y-1.5 text-sm">
        {sources.map((source) => (
          <li key={source.url}>
            <a
              href={source.url}
              target="_blank"
              rel="noreferrer noopener"
              className="underline decoration-[--rule] decoration-1 hover:decoration-[--accent]"
            >
              {source.label} ↗
            </a>
          </li>
        ))}
      </ul>
      <p className="mt-3 text-xs text-[--ink-faint] measure">
        Catatan disusun ulang dari sumber di atas dan tetap berstatus perlu
        verifikasi. Untuk jam buka dan harga tiket, periksa kanal resmi museum.
      </p>
    </section>
  );
}
