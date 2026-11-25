/**
 * Satu sumber tipe domain untuk aplikasi, skrip generator RDF, dan test.
 * MuseumRecord adalah bentuk baris di data/museums.json; MuseumDTO adalah
 * bentuk yang dikirim route handler ke UI setelah query SPARQL.
 */

export const PROVINCES = [
  "Aceh",
  "Sumatera Utara",
  "Sumatera Barat",
  "Riau",
  "Kepulauan Riau",
  "Jambi",
  "Bengkulu",
  "Sumatera Selatan",
  "Bangka Belitung",
  "Lampung",
] as const;

export type Province = (typeof PROVINCES)[number];

export const THEMES = [
  "perjuangan",
  "arkeologi",
  "etnografi",
  "seni-budaya",
  "sains-teknologi",
  "sejarah-alam",
] as const;

export type Theme = (typeof THEMES)[number];

export const THEME_LABELS: Record<Theme, string> = {
  perjuangan: "Perjuangan",
  arkeologi: "Arkeologi",
  etnografi: "Etnografi",
  "seni-budaya": "Seni & Budaya",
  "sains-teknologi": "Sains & Teknologi",
  "sejarah-alam": "Sejarah Alam",
};

export const ERAS = ["pra-kolonial", "kolonial", "kemerdekaan", "modern"] as const;

export type Era = (typeof ERAS)[number];

export const ERAS_LABELS: Record<Era, string> = {
  "pra-kolonial": "Pra-kolonial",
  kolonial: "Kolonial",
  kemerdekaan: "Kemerdekaan",
  modern: "Modern",
};

export const VERIFICATION_STATUSES = ["terverifikasi", "perlu-verifikasi"] as const;

export type VerificationStatus = (typeof VERIFICATION_STATUSES)[number];

/** Subklasifikasi ontologi museum; setiap museum minimal satu. */
export const MUSEUM_TYPES = ["StateMuseum", "SiteMuseum", "PrivateMuseum"] as const;

export type MuseumType = (typeof MUSEUM_TYPES)[number];

export const MUSEUM_TYPE_LABELS: Record<MuseumType, string> = {
  StateMuseum: "Museum Negeri",
  SiteMuseum: "Museum Situs",
  PrivateMuseum: "Museum Swasta",
};

/** Satu foto museum beserta kredit dan lisensinya. */
export interface MuseumImage {
  /** Path lokal (mis. /images/museums/slug/1.jpg) atau URL absolut. */
  src: string;
  alt: string;
  caption: string;
  /** Judul pendek yang ditampilkan di atas latar belakang foto. */
  title?: string | null;
  /** 2–3 kalimat tentang apa yang terlihat dan kaitannya dengan sejarah museum. */
  background?: string | null;
  /** Masa atau tarikh yang tampak pada foto, mis. "1915", "era 1970-an". */
  period?: string | null;
  /** 2–4 poin ringkas tentang apa yang layak diamati pada foto. */
  detail?: string[] | null;
  credit: string;
  license: string;
  licenseUrl: string | null;
  sourceUrl: string;
}

/** Satu bagian/isi pameran yang bisa dilihat pengunjung. */
export interface Exhibit {
  title: string;
  description: string;
  /** Masa atau tarikh benda, mis. "abad ke-15", "1915". */
  period?: string | null;
  /** Asal perolehan atau daerah benda berasal. */
  origin?: string | null;
  /** Bahan utama, mis. "perunggu", "kayu kemuning". */
  material?: string | null;
  /** Tandai bila benda termasuk andalan museum. */
  highlight?: boolean | null;
}

/** Sumber acuan yang dipakai untuk menulis catatan museum. */
export interface SourceRef {
  label: string;
  url: string;
}

/** Baris data sumber kebenaran (data/museums.json). */
export interface MuseumRecord {
  slug: string;
  name: string;
  city: string;
  province: Province | string;
  themes: (Theme | string)[];
  era: Era | string | null;
  establishedYear: number | null;
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  description: string;
  imageUrl: string | null;
  officialUrl: string | null;
  admissionNote: string | null;
  chapter: number;
  verificationStatus: VerificationStatus;
  /** Paragraf sejarah, ditampilkan berurutan. */
  history?: string[];
  /** Bagian/isi pameran yang menjadi andalan museum. */
  exhibits?: Exhibit[];
  /** Galeri foto berlisensi bebas; entri pertama dipakai sebagai gambar utama. */
  gallery?: MuseumImage[];
  /** Sumber yang dipakai untuk menyusun catatan museum. */
  sources?: SourceRef[];
  /** Subklasifikasi ontologi; minimal satu. */
  types?: MuseumType[];
  /** Kategori koleksi — hanya bila sumber menyebut eksplisit. */
  collections?: string[];
  /** Fasilitas — hanya bila sumber menyebut eksplisit. */
  facilities?: string[];
  /** Nama pendiri/tokoh (string), atau null. */
  founder?: string | null;
  governingBody?: string | null;
  openingHours?: string | null;
  collectionSize?: number | null;
  /** Status cagar budaya bila sumber menyebut; sering null. */
  heritage?: string | null;
  /** Slug museum terkait (relasi eksplisit); generator menulis dua arah. */
  relatedSlugs?: string[];
}

/** Bentuk yang dipakai UI setelah query SPARQL. */
export interface MuseumDTO {
  uri: string;
  slug: string;
  name: string;
  province: string | null;
  city: string | null;
  themes: string[];
  era: string | null;
  establishedYear: number | null;
  description: string | null;
  imageUrl: string | null;
  officialUrl: string | null;
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  admissionNote: string | null;
  verificationStatus: VerificationStatus;
  chapterIndex: number | null;
  chapterTitle: string | null;
  history: string[];
  exhibits: Exhibit[];
  gallery: MuseumImage[];
  sources: SourceRef[];
  types?: string[];
  collections?: string[];
  facilities?: string[];
  founder?: string | null;
  governingBody?: string | null;
  openingHours?: string | null;
  collectionSize?: number | null;
  heritage?: string | null;
  relatedSlugs?: string[];
}

export interface ChapterDTO {
  index: number;
  label: string;
  title: string;
  museumCount: number | null;
}

export interface RelatedDTO {
  uri: string;
  slug: string;
  name: string;
  city: string | null;
  province: string | null;
  themes: string[];
  score: number;
  reason: string;
}

export interface CatalogResponse {
  museums: MuseumDTO[];
  total: number;
  ranking?: { slug: string; score: number; group: "primary" | "secondary" }[];
}

export interface ChaptersResponse {
  chapters: ChapterDTO[];
}

export interface MuseumResponse {
  museum: MuseumDTO;
  related: RelatedDTO[];
}

export const FALLBACK_IMAGE = "/images/placeholder-museum.svg";

export const FUSEKI_DEFAULT_ENDPOINT = "http://localhost:3030/museum/query";

export function toSlug(name: string): string {
  return name
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function yearLabel(year: number | null | undefined): string {
  return year === null || year === undefined ? "Tahun tidak tercatat" : String(year);
}

export function themeLabels(themes: string[]): string[] {
  return themes.map((t) => THEME_LABELS[t as Theme] ?? t);
}

export function eraLabel(era: string | null): string {
  if (!era) return "Era tidak tercatat";
  return ERAS_LABELS[era as Era] ?? era;
}
