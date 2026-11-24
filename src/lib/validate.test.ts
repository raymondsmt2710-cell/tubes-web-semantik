import { describe, it, expect } from "vitest";
import { validateMuseums } from "./validate";
import type { MuseumRecord } from "./types";

const ok: MuseumRecord = {
  slug: "museum-ok",
  name: "Museum OK",
  city: "Banda Aceh",
  province: "Aceh",
  themes: ["etnografi"],
  era: "kolonial",
  establishedYear: 1930,
  address: "Jl. OK",
  latitude: 5.5,
  longitude: 95.3,
  description: "Deskripsi.",
  imageUrl: null,
  officialUrl: null,
  admissionNote: null,
  chapter: 1,
  verificationStatus: "terverifikasi",
};

describe("validateMuseums", () => {
  it("meloloskan data yang lengkap dan valid", () => {
    expect(validateMuseums([ok])).toHaveLength(0);
  });

  it("menandai museum tanpa provinsi sebagai error", () => {
    const issues = validateMuseums([{ ...ok, province: "" }]);
    expect(issues).toContainEqual(
      expect.objectContaining({ slug: "museum-ok", field: "province", level: "error" }),
    );
  });

  it("menandai provinsi di luar daftar resmi sebagai error", () => {
    const issues = validateMuseums([{ ...ok, province: "Jawa Barat" }]);
    expect(issues.some((i) => i.field === "province" && i.level === "error")).toBe(true);
  });

  it("menerima establishedYear null tanpa isu", () => {
    expect(validateMuseums([{ ...ok, establishedYear: null }])).toHaveLength(0);
  });

  it("menandai bab di luar rentang 1..7 sebagai error", () => {
    const issues = validateMuseums([{ ...ok, chapter: 9 }]);
    expect(issues.some((i) => i.field === "chapter" && i.level === "error")).toBe(true);
  });

  it("menandai tema di luar daftar resmi sebagai error", () => {
    const issues = validateMuseums([{ ...ok, themes: ["kuliner"] }]);
    expect(issues.some((i) => i.field === "themes" && i.level === "error")).toBe(true);
  });

  it("menandai koordinat di luar Pulau Sumatera sebagai error", () => {
    const luar = validateMuseums([{ ...ok, latitude: -7.0, longitude: 110.0 }]);
    expect(luar.some((i) => i.field === "latitude" && i.level === "error")).toBe(true);

    const dalam = validateMuseums([{ ...ok, latitude: 5.5, longitude: 95.3 }]);
    expect(dalam.some((i) => i.field === "latitude")).toBe(false);
  });

  it("memperingatkan museum yang belum terverifikasi", () => {
    const issues = validateMuseums([{ ...ok, verificationStatus: "perlu-verifikasi" }]);
    expect(issues).toHaveLength(1);
    expect(issues[0].level).toBe("warning");
    expect(issues[0].message).toMatch(/verifikasi/i);
  });

  it("menandai slug duplikat sebagai error pada entri kedua", () => {
    const issues = validateMuseums([ok, { ...ok }]);
    expect(issues.some((i) => i.field === "slug" && i.level === "error")).toBe(true);
  });

  it("menandai deskripsi kosong sebagai error", () => {
    const issues = validateMuseums([{ ...ok, description: "  " }]);
    expect(issues.some((i) => i.field === "description" && i.level === "error")).toBe(true);
  });
});

describe("validasi entitas baru", () => {
  it("menolak tipe yang tidak dikenal", () => {
    const issues = validateMuseums([{ ...ok, types: ["Bogus" as never] }]);
    expect(issues.some((i) => i.field === "types" && i.level === "error")).toBe(true);
  });

  it("menerima tipe sah", () => {
    const issues = validateMuseums([{ ...ok, types: ["StateMuseum", "SiteMuseum"] }]);
    expect(issues.some((i) => i.field === "types" && i.level === "error")).toBe(false);
  });

  it("menolak StateMuseum + PrivateMuseum sekaligus", () => {
    const issues = validateMuseums([{ ...ok, types: ["StateMuseum", "PrivateMuseum"] }]);
    expect(issues.some((i) => i.field === "types" && i.level === "error")).toBe(true);
  });

  it("menolak collectionSize negatif / bukan integer", () => {
    const neg = validateMuseums([{ ...ok, collectionSize: -1 }]);
    expect(neg.some((i) => i.field === "collectionSize" && i.level === "error")).toBe(true);
    const frac = validateMuseums([{ ...ok, collectionSize: 1.5 }]);
    expect(frac.some((i) => i.field === "collectionSize" && i.level === "error")).toBe(true);
  });

  it("menolak relatedSlugs yang menunjuk dirinya sendiri atau slug tak ada", () => {
    const self = validateMuseums([{ ...ok, relatedSlugs: ["museum-ok"] }]);
    expect(self.some((i) => i.field === "relatedSlugs" && i.level === "error")).toBe(true);
    const missing = validateMuseums([{ ...ok, relatedSlugs: ["tidak-ada"] }]);
    expect(missing.some((i) => i.field === "relatedSlugs" && i.level === "error")).toBe(true);
  });
});
