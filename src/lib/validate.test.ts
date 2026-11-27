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

    // Pulau Belitung (Bangka Belitung) berada di bujur ±108,2°.
    const belitung = validateMuseums([{ ...ok, latitude: -2.967, longitude: 108.164 }]);
    expect(belitung.some((i) => i.field === "latitude")).toBe(false);
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

describe("ambang kedalaman isi pameran dan galeri", () => {
  const panjang = (n: number) => "K".repeat(n);

  it("menandai deskripsi pameran yang terlalu pendek", () => {
    const issues = validateMuseums([
      { ...ok, exhibits: [{ title: "Lonceng", description: "Terlalu singkat." }] },
    ]);
    expect(issues).toContainEqual(
      expect.objectContaining({ field: "exhibits", level: "warning" }),
    );
  });

  it("meloloskan deskripsi pameran yang memenuhi ambang", () => {
    const issues = validateMuseums([
      { ...ok, exhibits: [{ title: "Lonceng", description: panjang(180) }] },
    ]);
    expect(issues.filter((i) => i.field === "exhibits")).toHaveLength(0);
  });

  it("menolak pameran tanpa judul", () => {
    const issues = validateMuseums([
      { ...ok, exhibits: [{ title: "  ", description: panjang(200) }] },
    ]);
    expect(issues).toContainEqual(
      expect.objectContaining({ field: "exhibits", level: "error" }),
    );
  });

  it("menandai latar belakang foto yang terlalu pendek", () => {
    const issues = validateMuseums([
      {
        ...ok,
        gallery: [
          {
            src: "/images/museums/museum-ok/1.jpg",
            alt: "Foto",
            caption: "Keterangan",
            background: "Pendek.",
            detail: ["Poin"],
            credit: "Seseorang",
            license: "CC BY-SA 4.0",
            licenseUrl: null,
            sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
          },
        ],
      },
    ]);
    expect(issues).toContainEqual(
      expect.objectContaining({ field: "gallery", level: "warning" }),
    );
  });

  it("menandai foto tanpa bidang detail", () => {
    const issues = validateMuseums([
      {
        ...ok,
        gallery: [
          {
            src: "/images/museums/museum-ok/1.jpg",
            alt: "Foto",
            caption: "Keterangan",
            background: panjang(240),
            credit: "Seseorang",
            license: "CC BY-SA 4.0",
            licenseUrl: null,
            sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
          },
        ],
      },
    ]);
    expect(issues).toContainEqual(
      expect.objectContaining({ field: "gallery", level: "warning" }),
    );
  });

  it("meloloskan foto yang latar dan detailnya lengkap", () => {
    const issues = validateMuseums([
      {
        ...ok,
        gallery: [
          {
            src: "/images/museums/museum-ok/1.jpg",
            alt: "Foto",
            caption: "Keterangan",
            background: panjang(240),
            detail: ["Poin pertama", "Poin kedua"],
            credit: "Seseorang",
            license: "CC BY-SA 4.0",
            licenseUrl: null,
            sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
          },
        ],
      },
    ]);
    expect(issues.filter((i) => i.field === "gallery")).toHaveLength(0);
  });

  it("menandai period foto yang tidak memuat penanda tarikh", () => {
    const issues = validateMuseums([
      {
        ...ok,
        gallery: [
          {
            src: "/images/museums/museum-ok/1.jpg",
            alt: "Foto",
            caption: "Keterangan",
            background: panjang(240),
            detail: ["Poin"],
            period: "bangunan museum provinsi",
            credit: "Seseorang",
            license: "CC BY-SA 4.0",
            licenseUrl: null,
            sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
          },
        ],
      },
    ]);
    expect(issues).toContainEqual(
      expect.objectContaining({ field: "gallery", level: "warning" }),
    );
  });

  it("meloloskan period foto yang berupa tarikh", () => {
    for (const period of ["1915", "abad ke-19", "era 1970-an", "masa kolonial", "sebelum 1905"]) {
      const issues = validateMuseums([
        {
          ...ok,
          gallery: [
            {
              src: "/images/museums/museum-ok/1.jpg",
              alt: "Foto",
              caption: "Keterangan",
              background: panjang(240),
              detail: ["Poin"],
              period,
              credit: "Seseorang",
              license: "CC BY-SA 4.0",
              licenseUrl: null,
              sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
            },
          ],
        },
      ]);
      expect(
        issues.filter((i) => i.field === "gallery" && i.message.includes("period")),
        `period "${period}" seharusnya diterima`,
      ).toHaveLength(0);
    }
  });

  it("menandai period pameran yang tidak memuat penanda tarikh", () => {
    const issues = validateMuseums([
      {
        ...ok,
        exhibits: [
          { title: "Lonceng", description: panjang(200), period: "benda andalan museum" },
        ],
      },
    ]);
    expect(issues).toContainEqual(
      expect.objectContaining({ field: "exhibits", level: "warning" }),
    );
  });
});
