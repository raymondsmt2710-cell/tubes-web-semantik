import {
  ERAS,
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
      }
    }

    if (record.verificationStatus === "perlu-verifikasi") {
      add(
        "verificationStatus",
        "warning",
        "Data belum diverifikasi; periksa nama, alamat, dan tahun berdiri.",
      );
    }
  }

  return issues;
}

export function hasErrors(issues: ValidationIssue[]): boolean {
  return issues.some((issue) => issue.level === "error");
}
