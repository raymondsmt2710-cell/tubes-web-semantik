import Link from "next/link";
import { CHAPTERS } from "@/lib/chapters";

interface ChapterListProps {
  counts?: Map<number, number> | null;
}

export default function ChapterList({ counts }: ChapterListProps) {
  return (
    <ol className="border-t border-[--rule]">
      {CHAPTERS.map((chapter) => {
        const count = counts?.get(chapter.index);
        return (
          <li key={chapter.index} className="border-b border-[--rule]">
            <Link
              href={`/jelajah/${chapter.index}`}
              className="entry-row flex items-baseline gap-4 px-1 sm:px-3"
            >
              <span className="label w-16 shrink-0">{chapter.label}</span>
              <span className="flex-1">
                <span className="font-serif text-lg sm:text-xl block">
                  {chapter.title}
                </span>
                <span className="text-xs text-[--ink-soft]">
                  {chapter.provinces.join(" · ")}
                </span>
              </span>
              <span className="label shrink-0 text-right">
                {count === undefined || count === null ? "—" : `${count} museum`}
              </span>
              <span aria-hidden className="text-[--ink-faint]">
                →
              </span>
            </Link>
          </li>
        );
      })}
    </ol>
  );
}
