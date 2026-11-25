import type { Exhibit } from "@/lib/types";

interface ExhibitListProps {
  exhibits: Exhibit[];
}

/**
 * Daftar isi pameran: bagian atau koleksi andalan yang bisa dilihat pengunjung.
 * Setiap entri membawa metadata ringkas (masa, asal, bahan) di bawah judul, dan
 * penanda "Andalan" untuk benda yang oleh museum dianggap paling penting.
 */
export default function ExhibitList({ exhibits }: ExhibitListProps) {
  if (exhibits.length === 0) {
    return (
      <p className="mt-3 text-sm text-[--ink-faint]">
        Rincian isi pameran museum ini belum tercatat.
      </p>
    );
  }

  return (
    <ol className="mt-4 m-0 p-0 list-none divide-y divide-[--rule] border-y border-[--rule]">
      {exhibits.map((exhibit, index) => {
        const meta = [exhibit.period, exhibit.origin, exhibit.material]
          .filter(Boolean)
          .join(" · ");

        return (
          <li
            key={`${exhibit.title}-${index}`}
            className="py-4 grid grid-cols-[2rem_1fr] gap-3"
          >
            <span className="label pt-1 tabular-nums">
              {String(index + 1).padStart(2, "0")}
            </span>
            <div>
              <div className="flex flex-wrap items-baseline gap-2">
                <h3 className="font-serif text-base leading-snug m-0">{exhibit.title}</h3>
                {exhibit.highlight && <span className="chip">Andalan</span>}
              </div>
              {meta && <p className="mt-1 text-xs text-[--ink-faint] m-0">{meta}</p>}
              {exhibit.description && (
                <p className="mt-1.5 text-sm text-[--ink-soft] leading-relaxed measure">
                  {exhibit.description}
                </p>
              )}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
