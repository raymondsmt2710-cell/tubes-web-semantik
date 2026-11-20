import type { Exhibit } from "@/lib/types";

interface ExhibitListProps {
  exhibits: Exhibit[];
}

/** Daftar isi pameran: bagian atau koleksi andalan yang bisa dilihat pengunjung. */
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
      {exhibits.map((exhibit, index) => (
        <li key={`${exhibit.title}-${index}`} className="py-3.5 grid grid-cols-[2rem_1fr] gap-3">
          <span className="label pt-1 tabular-nums">
            {String(index + 1).padStart(2, "0")}
          </span>
          <div>
            <h3 className="font-serif text-base leading-snug">{exhibit.title}</h3>
            {exhibit.description && (
              <p className="mt-1 text-sm text-[--ink-soft] leading-relaxed measure">
                {exhibit.description}
              </p>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}
