import Link from "next/link";
import { ROMAN } from "@/lib/chapters";

export interface IndexBoardItem {
  index: number;
  label: string;
  title: string;
  count: number | null;
  subtitle?: string;
  href: string;
}

interface IndexBoardProps {
  items: IndexBoardItem[];
  variant?: "cover" | "chapter";
}

/**
 * Papan indeks bergaya lemari katalog museum. Nomor romawi besar di kiri,
 * judul & provinsi di tengah, jumlah museum di kanan. Dipakai di sampul dan
 * di halaman bab.
 */
export default function IndexBoard({ items, variant = "cover" }: IndexBoardProps) {
  return (
    <div className="index-board">
      {items.map((item) => (
        <Link key={item.index} href={item.href} className="index-board-item">
          <span className="archive-number" aria-hidden>
            {item.label ? (ROMAN[item.index - 1] ?? String(item.index)) : String(item.index)}
          </span>
          <span className="min-w-0">
            <span className="font-serif text-lg sm:text-xl block leading-snug">
              {item.title}
            </span>
            {item.subtitle && (
              <span className="text-xs text-[--ink-soft]">{item.subtitle}</span>
            )}
          </span>
          <span className="label text-right whitespace-nowrap">
            {item.count === null ? "—" : `${item.count} museum`}
          </span>
          <span aria-hidden className="index-arrow text-[--ink-faint]">
            →
          </span>
        </Link>
      ))}
      {items.length === 0 && variant === "chapter" && (
        <p className="py-6 text-sm text-[--ink-soft]">Belum ada entri.</p>
      )}
    </div>
  );
}
