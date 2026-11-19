import Link from "next/link";
import { CHAPTERS } from "@/lib/chapters";

interface ChapterNavProps {
  current: number;
}

export default function ChapterNav({ current }: ChapterNavProps) {
  const previous = CHAPTERS.find((chapter) => chapter.index === current - 1);
  const next = CHAPTERS.find((chapter) => chapter.index === current + 1);

  return (
    <nav className="mt-12 flex flex-col sm:flex-row items-stretch justify-between gap-3 border-t border-[--rule] pt-6">
      <div className="flex-1">
        {previous ? (
          <Link href={`/jelajah/${previous.index}`} className="group block">
            <span className="label">← {previous.label}</span>
            <span className="block font-serif text-base group-hover:underline">
              {previous.title}
            </span>
          </Link>
        ) : (
          <Link href="/" className="label">
            ← Kembali ke sampul
          </Link>
        )}
      </div>

      <div className="sm:text-right flex-1">
        {next ? (
          <Link href={`/jelajah/${next.index}`} className="group block">
            <span className="label">{next.label} →</span>
            <span className="block font-serif text-base group-hover:underline">
              {next.title}
            </span>
          </Link>
        ) : (
          <Link href="/katalog" className="group block">
            <span className="label">Selesai →</span>
            <span className="block font-serif text-base group-hover:underline">
              Telusuri katalog lengkap
            </span>
          </Link>
        )}
      </div>
    </nav>
  );
}
