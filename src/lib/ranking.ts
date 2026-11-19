/** Ambang batas "hasil utama" pada pencarian teks. */
export const PRIMARY_THRESHOLD = 0.7;

/** Skor minimum agar sebuah baris masih layak ditampilkan sebagai hasil lain. */
export const SECONDARY_THRESHOLD = 0.15;

function normalize(value: string): string {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function initials(text: string): string {
  return text
    .split(/\s+/)
    .filter(Boolean)
    .map((word) => word[0])
    .join("");
}

function isSubsequence(needle: string, haystack: string): boolean {
  let index = 0;
  for (let i = 0; i < haystack.length && index < needle.length; i++) {
    if (haystack[i] === needle[index]) index++;
  }
  return index === needle.length && needle.length > 0;
}

/**
 * Skor kemiripan antara kata kunci dan nama museum (0..1).
 *
 * Peringkat sengaja dibuat bertingkat dan dapat dijelaskan: kecocokan persis,
 * awalan, akronim, lalu kemiripan huruf. Fungsi ini murni (tanpa I/O) supaya
 * perilakunya bisa diuji, dan hanya dijalankan atas kandidat yang sudah
 * dibatasi SPARQL.
 */
export function similarity(query: string, name: string): number {
  const q = normalize(query);
  const n = normalize(name);

  if (!q || !n) return 0;

  const compactName = n.replace(/\s+/g, "");
  const compactQuery = q.replace(/\s+/g, "");

  if (q === n || compactQuery === compactName) return 1;
  if (n.startsWith(q) || compactName.startsWith(compactQuery)) return 0.95;

  const wordInitials = initials(n);
  if (q === wordInitials || compactQuery === wordInitials) return 0.85;

  // Satu kata yang berdiri sendiri di dalam nama ("aceh" pada "Museum Negeri
  // Aceh") adalah kecocokan kuat, bukan sekadar potongan huruf.
  if (
    q.length >= 2 &&
    n.split(/\s+/).some((word) => word.length >= 2 && word.startsWith(q))
  ) {
    return 0.8;
  }

  // Query banyak kata ("museum aceh") dianggap kuat bila semua katanya muncul.
  const queryTokens = q.split(/\s+/).filter(Boolean);
  if (queryTokens.length > 1 && queryTokens.every((token) => n.includes(token))) {
    return 0.75;
  }

  const subsequenceScore = isSubsequence(compactQuery, compactName)
    ? 0.7 * (compactQuery.length / compactName.length)
    : 0;

  const substringScore = n.includes(q) ? 0.6 : 0;

  if (subsequenceScore > 0 || substringScore > 0) {
    return Math.max(subsequenceScore, substringScore);
  }

  const uniqueQueryChars = [...new Set(q.replace(/\s+/g, "").split(""))];
  const matches = uniqueQueryChars.filter((char) => n.includes(char)).length;
  return (matches / Math.max(uniqueQueryChars.length, n.length)) * 0.4;
}

export interface Ranked<T> {
  primary: T[];
  secondary: T[];
  scores: Map<string, number>;
}

/**
 * Memisahkan kandidat menjadi "hasil utama" (skor ≥ 0.7) dan "hasil lain".
 * Semua kandidat tetap dikembalikan supaya pengguna bisa melihat seluruh
 * hasil penyaringan; urutannya deterministik agar bisa diuji.
 */
export function rankMuseums<T extends { name: string }>(rows: T[], query: string): Ranked<T> {
  const trimmed = query.trim();
  const scores = new Map<string, number>();

  if (!trimmed) {
    const secondary = [...rows].sort((a, b) => a.name.localeCompare(b.name));
    for (const row of secondary) scores.set(row.name, 0);
    return { primary: [], secondary, scores };
  }

  const scored = rows.map((row) => {
    const score = similarity(trimmed, row.name);
    scores.set(row.name, score);
    return { row, score };
  });

  const byScore = (a: { score: number; row: T }, b: { score: number; row: T }) =>
    b.score - a.score || a.row.name.localeCompare(b.row.name);

  const primary = scored
    .filter((entry) => entry.score >= PRIMARY_THRESHOLD)
    .sort(byScore)
    .map((entry) => entry.row);

  const secondary = scored
    .filter((entry) => entry.score < PRIMARY_THRESHOLD)
    .sort(byScore)
    .map((entry) => entry.row);

  return { primary, secondary, scores };
}
