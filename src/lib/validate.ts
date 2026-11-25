import {
  ERAS,
  MUSEUM_TYPES,
  PROVINCES,
  THEMES,
  type MuseumRecord,
} from "./types";
import { CHAPTERS } from "./chapters";

export interface ValidationIssue {
  slug: string;
  field: string;
  level: "error" | "warning";
  message: string;
}

/** Kotak pembatas Pulau Sumatera; koordinat di luar ini hampir pasti salah. */
export const SUMATRA_BOUNDS = {
  minLat: -6.5,
  maxLat: 6.5,
  minLon: 94,
  maxLon: 107.5,
};

/** Ambang kedalaman teks; di bawah ini isi dianggap masih terlalu tipis. */
export const MIN_EXHIBIT_DESCRIPTION_CHARS = 180;
export const MIN_IMAGE_BACKGROUND_CHARS = 220;

/**
 * `period` haruslah tarikh atau masa, bukan topik. Bidang ini tampil di UI
 * sebagai label kecil yang dibaca pengunjung sebagai penanda waktu, sehingga
 * isinya perlu memuat penanda tarikh agar tidak menyesatkan.
 */
const PENANDA_TARIKH =
  /[0-9]|abad|era|masa|zaman|sebelum|sesudah|kini|modern|kolonial|prasejarah|megalitik|neolitik|paleolitik|klasik|perunggu|besi|kuno|purba/i;

export function periodBerupaTarikh(period: string): boolean {
  return PENANDA_TARIKH.test(period);
}

export function validateMuseums(records: MuseumRecord[]): ValidationIssue[] {
  const issues: ValidationIssue[] = [];
  const seen = new Set<string>();

  for (const record of records) {
    const slug = record.slug || "(tanpa-slug)";
    const add = (field: string, level: "error" | "warning", message: string) =>
      issues.push({ slug, field, level, message });

    if (!record.slug) add("slug", "error", "Slug kosong.");
    if (seen.has(record.slug)) {
      add("slug", "error", `Slug duplikat: "${record.slug}".`);
    }
    seen.add(record.slug);

    if (!record.name?.trim()) add("name", "error", "Nama museum kosong.");
    if (!record.description?.trim()) add("description", "error", "Deskripsi kosong.");

    if (!record.province?.trim()) {
      add("province", "error", "Provinsi kosong.");
    } else if (!(PROVINCES as readonly string[]).includes(record.province)) {
      add("province", "error", `Provinsi tidak dikenal: "${record.province}".`);
    }

    if (!record.city?.trim()) add("city", "error", "Kota/kabupaten kosong.");

    if (!Array.isArray(record.themes) || record.themes.length === 0) {
      add("themes", "error", "Tema kosong; setiap museum butuh minimal satu tema.");
    } else {
      for (const theme of record.themes) {
        if (!(THEMES as readonly string[]).includes(theme)) {
          add("themes", "error", `Tema tidak dikenal: "${theme}".`);
        }
      }
    }

    if (record.era && !(ERAS as readonly string[]).includes(record.era)) {
      add("era", "error", `Era tidak dikenal: "${record.era}".`);
    }

    if (
      !Number.isInteger(record.chapter) ||
      record.chapter < 1 ||
      record.chapter > CHAPTERS.length
    ) {
      add("chapter", "error", `Nomor bab di luar rentang 1..${CHAPTERS.length}.`);
    }

    if (
      record.establishedYear !== null &&
      record.establishedYear !== undefined &&
      (!Number.isInteger(record.establishedYear) ||
        record.establishedYear < 1000 ||
        record.establishedYear > new Date().getFullYear())
    ) {
      add("establishedYear", "error", `Tahun berdiri tidak wajar: ${record.establishedYear}.`);
    }

    const { latitude, longitude } = record;
    if (latitude !== null && longitude !== null) {
      const outside =
        latitude < SUMATRA_BOUNDS.minLat ||
        latitude > SUMATRA_BOUNDS.maxLat ||
        longitude < SUMATRA_BOUNDS.minLon ||
        longitude > SUMATRA_BOUNDS.maxLon;
      if (outside) {
        add(
          "latitude",
          "error",
          `Koordinat (${latitude}, ${longitude}) berada di luar Pulau Sumatera.`,
        );
      }
    }

    if (record.history || record.exhibits?.length || record.gallery?.length) {
      record.sources?.forEach((source, index) => {
        if (!source.url?.startsWith("http")) {
          add(
            "sources",
            "error",
            `Sumber ke-${index + 1} tidak memakai URL http(s): "${source.url}".`,
          );
        }
      });
      for (const [index, image] of (record.gallery ?? []).entries()) {
        if (!image.src) {
          add("gallery", "error", `Foto ke-${index + 1} tidak punya src.`);
        }
        if (!image.license) {
          add(
            "gallery",
            "warning",
            `Foto ke-${index + 1} tidak mencantumkan lisensi; kredit wajib jelas.`,
          );
        }
        if (!image.sourceUrl) {
          add("gallery", "warning", `Foto ke-${index + 1} tidak mencantumkan tautan sumber.`);
        }
        const panjangLatar = image.background?.trim().length ?? 0;
        if (panjangLatar < MIN_IMAGE_BACKGROUND_CHARS) {
          add(
            "gallery",
            "warning",
            `Foto ke-${index + 1} latar belakangnya ${panjangLatar} karakter; minimal ${MIN_IMAGE_BACKGROUND_CHARS}.`,
          );
        }
        if (!image.detail?.length) {
          add("gallery", "warning", `Foto ke-${index + 1} belum punya poin pengamatan (detail).`);
        }
        if (image.period && !periodBerupaTarikh(image.period)) {
          add(
            "gallery",
            "warning",
            `Foto ke-${index + 1} period "${image.period}" bukan tarikh; pindahkan topiknya ke title/detail.`,
          );
        }
      }
      for (const [index, exhibit] of (record.exhibits ?? []).entries()) {
        if (!exhibit.title?.trim()) {
          add("exhibits", "error", `Pameran ke-${index + 1} tidak punya judul.`);
        }
        const panjangDeskripsi = exhibit.description?.trim().length ?? 0;
        if (panjangDeskripsi < MIN_EXHIBIT_DESCRIPTION_CHARS) {
          add(
            "exhibits",
            "warning",
            `Pameran ke-${index + 1} ("${exhibit.title}") baru ${panjangDeskripsi} karakter; minimal ${MIN_EXHIBIT_DESCRIPTION_CHARS}.`,
          );
        }
        if (exhibit.period && !periodBerupaTarikh(exhibit.period)) {
          add(
            "exhibits",
            "warning",
            `Pameran ke-${index + 1} ("${exhibit.title}") period "${exhibit.period}" bukan tarikh.`,
          );
        }
      }
    }

    if (record.verificationStatus === "perlu-verifikasi") {
      add(
        "verificationStatus",
        "warning",
        "Data belum diverifikasi; periksa nama, alamat, dan tahun berdiri.",
      );
    }

    if (record.types !== undefined) {
      if (record.types.length === 0) {
        add("types", "error", "Museum harus punya minimal satu tipe.");
      } else {
        for (const t of record.types) {
          if (!(MUSEUM_TYPES as readonly string[]).includes(t)) {
            add("types", "error", `Tipe tidak dikenal: "${t}".`);
          }
        }
        if (record.types.includes("StateMuseum") && record.types.includes("PrivateMuseum")) {
          add("types", "error", "StateMuseum dan PrivateMuseum tidak boleh bersamaan.");
        }
      }
    }

    if (
      record.collectionSize !== null &&
      record.collectionSize !== undefined &&
      (!Number.isInteger(record.collectionSize) || record.collectionSize < 0)
    ) {
      add("collectionSize", "error", `Ukuran koleksi tidak sah: ${record.collectionSize}.`);
    }
  }

  const allSlugs = new Set(records.map((r) => r.slug));
  for (const record of records) {
    for (const target of record.relatedSlugs ?? []) {
      if (target === record.slug) {
        issues.push({
          slug: record.slug,
          field: "relatedSlugs",
          level: "error",
          message: "Museum tidak boleh menautkan dirinya sendiri.",
        });
      } else if (!allSlugs.has(target)) {
        issues.push({
          slug: record.slug,
          field: "relatedSlugs",
          level: "error",
          message: `Museum terkait tidak ditemukan: "${target}".`,
        });
      }
    }
  }

  return issues;
}

export function hasErrors(issues: ValidationIssue[]): boolean {
  return issues.some((issue) => issue.level === "error");
}
