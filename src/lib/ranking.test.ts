import { describe, it, expect } from "vitest";
import { similarity, rankMuseums, PRIMARY_THRESHOLD } from "./ranking";

describe("similarity", () => {
  it("memberi skor 1 untuk kecocokan persis tanpa peduli kapitalisasi", () => {
    expect(similarity("museum negeri aceh", "Museum Negeri Aceh")).toBe(1);
  });

  it("memberi skor tinggi untuk awalan nama", () => {
    expect(similarity("museum n", "Museum Negeri Aceh")).toBeGreaterThanOrEqual(0.95);
  });

  it("mengenali akronim huruf awal tiap kata", () => {
    expect(similarity("mna", "Museum Negeri Aceh")).toBeGreaterThanOrEqual(0.85);
  });

  it("mengenali awalan yang melewati spasi", () => {
    expect(similarity("museumn", "Museum Negeri Aceh")).toBeGreaterThanOrEqual(0.95);
  });

  it("mengenali satu kata yang muncul di tengah nama", () => {
    expect(similarity("aceh", "Museum Negeri Aceh")).toBeGreaterThanOrEqual(
      PRIMARY_THRESHOLD,
    );
    expect(similarity("timah", "Museum Timah Indonesia")).toBeGreaterThanOrEqual(
      PRIMARY_THRESHOLD,
    );
  });

  it("memberi skor 0.6 untuk potongan yang bukan kata utuh", () => {
    expect(similarity("seum", "Museum Negeri Aceh")).toBeCloseTo(0.6, 5);
  });

  it("memberi skor rendah untuk nama yang tidak berhubungan", () => {
    expect(similarity("timah", "Museum Tsunami Aceh")).toBeLessThan(PRIMARY_THRESHOLD);
  });

  it("tidak meledak untuk nama kosong", () => {
    expect(similarity("aceh", "")).toBe(0);
    expect(similarity("", "Museum Aceh")).toBe(0);
  });
});

describe("rankMuseums", () => {
  const rows = [
    { name: "Museum Negeri Aceh" },
    { name: "Museum Tsunami Aceh" },
    { name: "Museum Timah Indonesia" },
  ];

  it("menaruh hasil di atas ambang ke kelompok utama", () => {
    const { primary } = rankMuseums(rows, "museum negeri aceh");
    expect(primary[0].name).toBe("Museum Negeri Aceh");
  });

  it("mengurutkan hasil utama dari skor tertinggi", () => {
    const { primary } = rankMuseums(rows, "museum aceh");
    expect(primary.length).toBeGreaterThan(0);
    expect(primary[0].name).toMatch(/Aceh/);
  });

  it("tidak membuang hasil saat query kosong", () => {
    const { primary, secondary } = rankMuseums(rows, "   ");
    expect(primary).toHaveLength(0);
    expect(secondary).toHaveLength(3);
  });

  it("tetap mengembalikan semua baris pada kelompok sekunder", () => {
    const { primary, secondary } = rankMuseums(rows, "aceh");
    expect(primary.length + secondary.length).toBe(3);
  });

  it("deterministik: skor seri diurutkan berdasarkan nama", () => {
    const seri = [{ name: "Museum B" }, { name: "Museum A" }];
    const { secondary } = rankMuseums(seri, "zzz");
    expect(secondary.map((r) => r.name)).toEqual(["Museum A", "Museum B"]);
  });

  it("menaikkan kecocokan kota/tema ke hasil utama lewat searchText", () => {
    const rows = [
      { name: "Museum Negeri Sumatera Utara", hay: "medan sumatera utara" },
      { name: "Museum Timah Indonesia", hay: "pangkalpinang bangka belitung" },
    ];
    const { primary } = rankMuseums(rows, "medan", (row) => row.hay);
    expect(primary.map((row) => row.name)).toEqual([
      "Museum Negeri Sumatera Utara",
    ]);
  });

  it("nama tetap lebih tinggi daripada kecocokan field", () => {
    const rows = [
      { name: "Museum Medan", hay: "medan" },
      { name: "Museum Lain", hay: "medan" },
    ];
    const { scores } = rankMuseums(rows, "medan", (row) => row.hay);
    expect(scores.get("Museum Medan")).toBeGreaterThan(
      scores.get("Museum Lain") ?? 0,
    );
  });
});
