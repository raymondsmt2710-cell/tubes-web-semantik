import Link from "next/link";
import { themeLabels, yearLabel, type MuseumDTO } from "@/lib/types";

interface MuseumEntryProps {
  museum: MuseumDTO;
  index?: number;
}

export default function MuseumEntry({ museum, index }: MuseumEntryProps) {
  const meta = [museum.city, museum.province, yearLabel(museum.establishedYear)]
    .filter(Boolean)
    .join(" · ");

  return (
    <Link href={`/museum/${encodeURIComponent(museum.slug)}`} className="entry-row px-1 sm:px-3">
      <div className="flex items-baseline gap-4">
        {index !== undefined && (
          <span className="label w-7 shrink-0 tabular-nums">
            {String(index).padStart(2, "0")}
          </span>
        )}
        <div className="flex-1 min-w-0">
          <h3 className="font-serif text-lg sm:text-xl leading-snug">{museum.name}</h3>
          <p className="text-xs text-[--ink-soft] mt-1">{meta}</p>
          <div className="mt-2 flex flex-wrap gap-1.5">
            {themeLabels(museum.themes).map((theme) => (
              <span key={theme} className="chip">
                {theme}
              </span>
            ))}
          </div>
        </div>
        <span aria-hidden className="text-[--ink-faint] shrink-0">
          →
        </span>
      </div>
    </Link>
  );
}
