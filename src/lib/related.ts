import type { MuseumDTO, RelatedDTO } from "./types";
import { THEME_LABELS, type Theme } from "./types";

const THEME_WEIGHT = 3;
const CITY_WEIGHT = 2;
const ERA_WEIGHT = 1;
const CHAPTER_WEIGHT = 1;

function themeLabel(theme: string): string {
  return THEME_LABELS[theme as Theme] ?? theme;
}

export interface RelationScore {
  score: number;
  reason: string;
}

/**
 * Menghitung kedekatan dua museum dari relasi graf (bukan dari teks).
 * Bobot tertulis di sini supaya hasilnya bisa dijelaskan kepada pengguna
 * dan diuji secara deterministik.
 */
export function scoreRelated(base: MuseumDTO, candidate: MuseumDTO): RelationScore {
  let score = 0;
  const reasons: string[] = [];

  const sharedThemes = candidate.themes.filter((theme) => base.themes.includes(theme));
  if (sharedThemes.length > 0) {
    score += sharedThemes.length * THEME_WEIGHT;
    reasons.push(`satu tema (${sharedThemes.map(themeLabel).join(", ")})`);
  }

  if (base.city && candidate.city && base.city === candidate.city) {
    score += CITY_WEIGHT;
    reasons.push(`satu kota (${base.city})`);
  }

  if (base.era && candidate.era && base.era === candidate.era) {
    score += ERA_WEIGHT;
    reasons.push(`satu era (${base.era})`);
  }

  if (
    base.chapterIndex !== null &&
    candidate.chapterIndex !== null &&
    Math.abs(base.chapterIndex - candidate.chapterIndex) === 1
  ) {
    score += CHAPTER_WEIGHT;
    reasons.push("bab yang bersebelahan dalam alur");
  }

  return { score, reason: reasons.join("; ") };
}

/**
 * Memilih museum yang layak ditampilkan sebagai "benang merah".
 * Kandidat berskor 0 tidak pernah ditampilkan, museum itu sendiri selalu
 * dibuang, dan urutan akhirnya deterministik.
 */
export function pickRelated(
  base: MuseumDTO,
  candidates: MuseumDTO[],
  limit = 6,
): RelatedDTO[] {
  return candidates
    .filter((candidate) => candidate.slug !== base.slug)
    .map((candidate) => ({ candidate, ...scoreRelated(base, candidate) }))
    .filter((entry) => entry.score > 0)
    .sort(
      (a, b) =>
        b.score - a.score || a.candidate.name.localeCompare(b.candidate.name),
    )
    .slice(0, limit)
    .map((entry) => ({
      uri: entry.candidate.uri,
      slug: entry.candidate.slug,
      name: entry.candidate.name,
      city: entry.candidate.city,
      province: entry.candidate.province,
      themes: entry.candidate.themes,
      score: entry.score,
      reason: entry.reason,
    }));
}
