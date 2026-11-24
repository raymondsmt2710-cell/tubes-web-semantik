import { MUSEUM_TYPE_LABELS, type MuseumType } from "@/lib/types";

interface MuseumTypeBadgeProps {
  types: string[] | undefined;
  className?: string;
}

/**
 * Menampilkan subklasifikasi ontologi museum (Museum Negeri/Situs/Swasta).
 * Sebuah museum bisa punya lebih dari satu tipe (mis. Situs + Negeri).
 */
export default function MuseumTypeBadge({ types, className }: MuseumTypeBadgeProps) {
  const valid = (types ?? []).filter(
    (t): t is MuseumType => t in MUSEUM_TYPE_LABELS,
  );
  if (valid.length === 0) return null;

  return (
    <span className={`inline-flex flex-wrap gap-1.5 ${className ?? ""}`}>
      {valid.map((type) => (
        <span
          key={type}
          className="chip"
          style={{ background: "var(--gold-soft)", borderColor: "var(--gold)", color: "var(--gold-ink)" }}
        >
          {MUSEUM_TYPE_LABELS[type]}
        </span>
      ))}
    </span>
  );
}
