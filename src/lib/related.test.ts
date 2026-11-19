import { describe, it, expect } from "vitest";
import { pickRelated, scoreRelated } from "./related";
import type { MuseumDTO } from "./types";

function museum(overrides: Partial<MuseumDTO> = {}): MuseumDTO {
  return {
    uri: "https://museumsumatera.id/resource/museum/base",
    slug: "base",
    name: "Museum Dasar",
    province: "Aceh",
    city: "Banda Aceh",
    themes: ["etnografi"],
    era: "kolonial",
    establishedYear: 1915,
    description: null,
    imageUrl: null,
    officialUrl: null,
    address: null,
    latitude: null,
    longitude: null,
    admissionNote: null,
    verificationStatus: "perlu-verifikasi",
    chapterIndex: 1,
    chapterTitle: "Dari Pelabuhan ke Pedalaman",
    ...overrides,
  };
}

describe("scoreRelated", () => {
  it("memberi +3 per tema yang sama", () => {
    const candidate = museum({
      slug: "x",
      themes: ["etnografi"],
      city: "Lhokseumawe",
      era: "modern",
    });
    const result = scoreRelated(museum(), candidate);
    expect(result.score).toBe(3);
    expect(result.reason).toMatch(/tema/i);
  });

  it("menjumlahkan bobot beberapa tema yang sama", () => {
    const base = museum({ themes: ["etnografi", "perjuangan"] });
    const candidate = museum({
      slug: "x",
      themes: ["etnografi", "perjuangan"],
      city: "Lhokseumawe",
      era: "modern",
    });
    expect(scoreRelated(base, candidate).score).toBe(6);
  });

  it("memberi +2 untuk kota yang sama", () => {
    const candidate = museum({
      slug: "x",
      city: "Banda Aceh",
      themes: ["arkeologi"],
      era: "modern",
    });
    const result = scoreRelated(museum(), candidate);
    expect(result.score).toBe(2);
    expect(result.reason).toMatch(/kota/i);
  });

  it("memberi +1 untuk era yang sama", () => {
    const candidate = museum({
      slug: "x",
      themes: ["arkeologi"],
      city: "Lhokseumawe",
      era: "kolonial",
    });
    expect(scoreRelated(museum(), candidate).score).toBe(1);
  });

  it("memberi +1 untuk bab yang bersebelahan", () => {
    const candidate = museum({
      slug: "x",
      themes: ["arkeologi"],
      city: "Medan",
      era: "modern",
      province: "Sumatera Utara",
      chapterIndex: 2,
    });
    const result = scoreRelated(museum(), candidate);
    expect(result.score).toBe(1);
    expect(result.reason).toMatch(/bab/i);
  });

  it("memberi skor 0 untuk museum yang tidak berhubungan", () => {
    const candidate = museum({
      slug: "x",
      themes: ["sains-teknologi"],
      city: "Palembang",
      era: "modern",
      province: "Sumatera Selatan",
      chapterIndex: 6,
    });
    expect(scoreRelated(museum(), candidate).score).toBe(0);
  });

  it("tidak menghitung bab yang jauh lebih dari satu", () => {
    const candidate = museum({
      slug: "x",
      themes: ["arkeologi"],
      city: "Bandar Lampung",
      era: "modern",
      chapterIndex: 7,
    });
    expect(scoreRelated(museum(), candidate).score).toBe(0);
  });
});

describe("pickRelated", () => {
  it("menyusun alasan dalam Bahasa Indonesia yang bisa dibaca", () => {
    const [related] = pickRelated(museum(), [museum({ slug: "x", name: "Museum X" })]);
    expect(related.reason).toMatch(/tema/i);
    expect(related.reason).toMatch(/etnografi/i);
  });

  it("tidak pernah merekomendasikan museum itu sendiri", () => {
    const result = pickRelated(museum(), [museum()]);
    expect(result.some((r) => r.slug === "base")).toBe(false);
  });

  it("menyembunyikan kandidat berskor 0", () => {
    const unrelated = museum({
      slug: "z",
      themes: ["sains-teknologi"],
      city: "Pangkalpinang",
      era: "modern",
      chapterIndex: 6,
    });
    expect(pickRelated(museum(), [unrelated])).toHaveLength(0);
  });

  it("membatasi jumlah rekomendasi secara default menjadi 6", () => {
    const candidates = Array.from({ length: 10 }, (_, i) =>
      museum({ slug: `c${i}`, name: `Museum C${i}` }),
    );
    expect(pickRelated(museum(), candidates)).toHaveLength(6);
  });

  it("deterministik: skor seri diurutkan berdasarkan nama", () => {
    const candidates = [
      museum({ slug: "b", name: "Museum B" }),
      museum({ slug: "a", name: "Museum A" }),
    ];
    const result = pickRelated(museum(), candidates);
    expect(result.map((r) => r.name)).toEqual(["Museum A", "Museum B"]);
  });

  it("mengurutkan dari skor tertinggi", () => {
    const kuat = museum({ slug: "kuat", name: "Museum Kuat", themes: ["etnografi", "perjuangan"] });
    const lemah = museum({
      slug: "lemah",
      name: "Museum Lemah",
      themes: ["arkeologi"],
      city: "Medan",
      era: "modern",
      chapterIndex: 2,
    });
    const result = pickRelated(museum(), [lemah, kuat]);
    expect(result[0].slug).toBe("kuat");
    expect(result.every((r) => r.score > 0)).toBe(true);
  });
});
