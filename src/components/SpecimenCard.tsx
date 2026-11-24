import Link from "next/link";
import MuseumImage from "@/components/MuseumImage";
import MuseumTypeBadge from "@/components/MuseumTypeBadge";
import VerificationBadge from "@/components/VerificationBadge";
import { eraLabel, themeLabels, yearLabel, type MuseumDTO } from "@/lib/types";

interface SpecimenCardProps {
  museum: MuseumDTO;
  archiveNumber?: string;
}

function MetaRow({ label, value, mono }: { label: string; value: React.ReactNode; mono?: boolean }) {
  return (
    <>
      <dt>{label}</dt>
      <dd className={mono ? "mono" : undefined}>{value}</dd>
    </>
  );
}

/**
 * Lembar katalog bergaya specimen card museum: nomor arsip, judul, plate foto
 * berlabel, dan tabel metadata presisi. Nilai yang tidak tersedia ditandai
 * netral ("Tidak tercatat"), bukan disembunyikan, agar lembar terasa lengkap.
 */
export default function SpecimenCard({ museum, archiveNumber }: SpecimenCardProps) {
  const themes = themeLabels(museum.themes);

  return (
    <article className="specimen-card p-5 sm:p-8">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="label">
            {[museum.city, museum.province].filter(Boolean).join(" · ") || "Lokasi tidak tercatat"}
          </p>
          <h1 className="mt-2 text-3xl sm:text-4xl max-w-2xl">{museum.name}</h1>
        </div>
        {archiveNumber && (
          <span className="archive-number shrink-0" aria-hidden>
            {archiveNumber}
          </span>
        )}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <VerificationBadge status={museum.verificationStatus} />
        <MuseumTypeBadge types={museum.types} />
        {themes.map((theme) => (
          <span key={theme} className="chip">
            {theme}
          </span>
        ))}
      </div>

      <div className="mt-8 grid gap-x-10 gap-y-8 sm:grid-cols-[1.35fr_1fr]">
        <div>
          <MuseumImage src={museum.imageUrl} alt={`Museum ${museum.name}`} />

          {museum.description && (
            <section className="mt-8">
              <h2 className="text-lg">Catatan koleksi</h2>
              <p className="mt-3 text-[--ink-soft] leading-relaxed measure">
                {museum.description}
              </p>
            </section>
          )}
        </div>

        <aside>
          <h2 className="text-lg mb-2">Lembar data</h2>
          <dl className="meta-table grid grid-cols-[6.5rem_1fr] gap-x-3 m-0">
            <MetaRow label="Kota" value={museum.city ?? "Tidak tercatat"} />
            <MetaRow label="Provinsi" value={museum.province ?? "Tidak tercatat"} />
            <MetaRow label="Berdiri" value={yearLabel(museum.establishedYear)} mono />
            <MetaRow label="Era" value={eraLabel(museum.era)} />
            <MetaRow label="Tema" value={themes.length > 0 ? themes.join(", ") : "Tidak tercatat"} />
            {museum.collectionSize !== null && museum.collectionSize !== undefined && (
              <MetaRow
                label="Koleksi"
                value={`${museum.collectionSize.toLocaleString("id-ID")} benda`}
                mono
              />
            )}
            {museum.governingBody && <MetaRow label="Pengelola" value={museum.governingBody} />}
            {museum.founder && <MetaRow label="Pendiri" value={museum.founder} />}
            {museum.openingHours && <MetaRow label="Jam buka" value={museum.openingHours} mono />}
            <MetaRow label="Alamat" value={museum.address ?? "Tidak tercatat"} />
            <MetaRow
              label="Kunjungan"
              value={museum.admissionNote ?? "Belum ada catatan kunjungan."}
            />
          </dl>

          {museum.officialUrl && (
            <p className="mt-4 text-sm">
              <a
                href={museum.officialUrl}
                target="_blank"
                rel="noreferrer noopener"
                className="underline decoration-[--accent]"
              >
                Situs resmi museum ↗
              </a>
            </p>
          )}

          <p className="mt-4 text-xs text-[--ink-faint] measure">
            Data ini disusun untuk pembelajaran. Periksa jam buka dan koleksi pada
            sumber resmi sebelum berkunjung.
          </p>
        </aside>
      </div>

      {museum.chapterIndex !== null && museum.chapterTitle && (
        <p className="mt-8 text-sm">
          <Link
            href={`/jelajah/${museum.chapterIndex}`}
            className="underline decoration-[--rule]"
          >
            Bagian dari alur pameran bab {museum.chapterIndex}: {museum.chapterTitle} →
          </Link>
        </p>
      )}
    </article>
  );
}
