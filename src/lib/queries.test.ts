import { describe, it, expect } from "vitest";
import {
  chaptersQuery,
  museumsByChapterQuery,
  searchCatalogQuery,
  museumBySlugQuery,
  relatedCandidatesQuery,
  mapMuseumRow,
  loadRowsOrNull,
  museumExhibitsQuery,
  museumImagesQuery,
  mapExhibitRow,
  mapGalleryRows,
} from "./queries";
import type { SparqlBinding } from "./sparql";

describe("searchCatalogQuery", () => {
  it("menyaring provinsi di dalam SPARQL, bukan setelahnya", () => {
    const q = searchCatalogQuery({ province: "Aceh" });
    // Label provinsi bertanda bahasa (@id), jadi perbandingan harus lewat STR().
    expect(q).toContain('FILTER(STR(?province) = "Aceh")');
  });

  it("kata kunci q juga mencocokkan koleksi dan fasilitas di dalam SPARQL", () => {
    const q = searchCatalogQuery({ q: "etnografi" });
    expect(q).toContain("?collections");
    expect(q).toContain("?facilities");
  });

  it("selalu membatasi hasil dengan LIMIT 300", () => {
    expect(searchCatalogQuery({})).toContain("LIMIT 300");
  });

  it("meng-escape tanda kutip pada input provinsi", () => {
    const q = searchCatalogQuery({ province: 'Aceh" OR 1=1' });
    expect(q).toContain('\\"');
    expect(q).not.toContain('"Aceh" OR 1=1"');
  });

  it("mengurutkan tahun menurun dan menaruh museum tanpa tahun di akhir", () => {
    expect(searchCatalogQuery({ sort: "year", order: "desc" })).toMatch(
      /ORDER BY \(BOUND\(\?year\) = false\) DESC\(\?year\)/i,
    );
  });

  it("memakai ORDER BY ASC(?name) secara default", () => {
    expect(searchCatalogQuery({})).toMatch(/ORDER BY ASC\(\?name\)/i);
  });

  it("tidak menambahkan filter tema bila tema kosong", () => {
    expect(searchCatalogQuery({})).not.toContain("themeFilterLabel");
  });

  it("menyaring tema dengan FILTER EXISTS agar museum multi-tema tetap utuh", () => {
    const q = searchCatalogQuery({ theme: "etnografi" });
    expect(q).toContain("FILTER EXISTS");
    expect(q).toContain('FILTER(STR(?themeFilterLabel) = "etnografi")');
  });

  it("menyaring tahun minimum dengan FILTER numerik", () => {
    const q = searchCatalogQuery({ minYear: 1900 });
    expect(q).toContain("?year >= 1900");
  });

  it("menyaring era dengan FILTER", () => {
    const q = searchCatalogQuery({ era: "kolonial" });
    expect(q).toContain('FILTER(STR(?era) = "kolonial")');
  });

  it("mengabaikan minYear yang bukan bilangan", () => {
    const q = searchCatalogQuery({ minYear: Number.NaN });
    expect(q).not.toContain("?year >=");
  });

  it("mencari q di nama, kota, provinsi, tema, era, dan deskripsi di dalam SPARQL", () => {
    const q = searchCatalogQuery({ q: "medan" });
    expect(q).toContain('CONTAINS(LCASE(STR(?name)), "medan")');
    expect(q).toContain('CONTAINS(LCASE(COALESCE(STR(?city), "")), "medan")');
    expect(q).toContain(
      'CONTAINS(LCASE(COALESCE(STR(?province), "")), "medan")',
    );
    expect(q).toContain('CONTAINS(LCASE(COALESCE(STR(?themes), "")), "medan")');
    expect(q).toContain('CONTAINS(LCASE(COALESCE(STR(?era), "")), "medan")');
    expect(q).toContain(
      'CONTAINS(LCASE(COALESCE(STR(?description), "")), "medan")',
    );
  });

  it("memecah q banyak kata menjadi beberapa filter yang semuanya harus cocok", () => {
    const q = searchCatalogQuery({ q: "museum aceh" });
    expect(q).toContain('"museum"');
    expect(q).toContain('"aceh"');
    expect(q.match(/CONTAINS\(LCASE\(STR\(\?name\)\)/g)).toHaveLength(2);
  });

  it("tidak menambahkan filter teks saat q kosong", () => {
    expect(searchCatalogQuery({ q: "   " })).not.toContain("CONTAINS");
  });

  it("meng-escape tanda kutip pada q", () => {
    expect(searchCatalogQuery({ q: 'x"y' })).toContain('\\"');
  });
});

describe("museumsByChapterQuery", () => {
  it("membatasi hasil pada nomor bab yang diminta", () => {
    const q = museumsByChapterQuery(3);
    expect(q).toContain("FILTER(?chapterIndex = 3)");
  });

  it("menolak nomor bab di luar 1..7", () => {
    expect(() => museumsByChapterQuery(0)).toThrow(/bab/i);
    expect(() => museumsByChapterQuery(8)).toThrow(/bab/i);
    expect(() => museumsByChapterQuery(1.5)).toThrow(/bab/i);
  });
});

describe("chaptersQuery", () => {
  it("menghitung jumlah museum per bab dengan COUNT", () => {
    const q = chaptersQuery();
    expect(q).toContain("COUNT(?museum)");
    expect(q).toContain("GROUP BY");
  });
});

describe("museumBySlugQuery / relatedCandidatesQuery", () => {
  it("mencari museum lewat segmen terakhir URI", () => {
    expect(museumBySlugQuery("museum-negeri-aceh")).toContain("museum-negeri-aceh");
    expect(museumBySlugQuery("museum-negeri-aceh")).toContain("LIMIT 1");
  });

  it("meng-escape slug yang berisi tanda kutip", () => {
    expect(museumBySlugQuery('x"y')).toContain('\\"');
  });

  it("kandidat terkait mengecualikan museum itu sendiri di dalam SPARQL", () => {
    const q = relatedCandidatesQuery("museum-negeri-aceh");
    expect(q).toContain("FILTER(?slug != \"museum-negeri-aceh\")");
  });
});

describe("mapMuseumRow", () => {
  it("memetakan binding SPARQL ke MuseumDTO lengkap", () => {
    const dto = mapMuseumRow({
      museum: { type: "uri", value: "https://museumsumatera.id/resource/museum/x" },
      slug: { type: "literal", value: "x" },
      name: { type: "literal", value: "Museum X" },
      province: { type: "literal", value: "Aceh" },
      themes: { type: "literal", value: "etnografi|perjuangan" },
      year: { type: "literal", value: "1930" },
      chapterIndex: { type: "literal", value: "1" },
    });

    expect(dto).toMatchObject({
      uri: "https://museumsumatera.id/resource/museum/x",
      slug: "x",
      name: "Museum X",
      province: "Aceh",
      themes: ["etnografi", "perjuangan"],
      establishedYear: 1930,
      chapterIndex: 1,
      city: null,
      verificationStatus: "perlu-verifikasi",
    });
  });

  it("tidak meledak saat tahun atau tema tidak ada", () => {
    const dto = mapMuseumRow({ name: { type: "literal", value: "Museum Y" } });
    expect(dto.establishedYear).toBeNull();
    expect(dto.themes).toEqual([]);
    expect(dto.establishedYear).not.toBe(0);
  });

  it("memetakan types, collections, dan collectionSize", () => {
    const dto = mapMuseumRow({
      museum: { type: "uri", value: "https://museumsumatera.id/resource/museum/x" },
      name: { type: "literal", value: "Museum X" },
      types: { type: "literal", value: "StateMuseum|SiteMuseum" },
      collections: { type: "literal", value: "etnografika|filologika" },
      collectionSize: { type: "literal", value: "6038" },
    });
    expect(dto.types).toEqual(["StateMuseum", "SiteMuseum"]);
    expect(dto.collections).toEqual(["etnografika", "filologika"]);
    expect(dto.collectionSize).toBe(6038);
  });
});

describe("query katalog: types via GROUP_CONCAT", () => {
  it("mengumpulkan types tanpa menggandakan baris", () => {
    const q = searchCatalogQuery({});
    expect(q).toContain("GROUP_CONCAT");
    expect(q).toContain("?types");
    // tipe tidak boleh jadi pola OPTIONAL bebas di blok utama
    expect(q).not.toMatch(/\?museum\s+a\s+\?type\b/);
  });
});

describe("properti kedalaman pameran dan galeri", () => {
  it("menarik properti kedalaman pada kueri pameran", () => {
    const q = museumExhibitsQuery("museum-uji");
    expect(q).toContain("sdp:exhibitPeriod");
    expect(q).toContain("sdp:exhibitOrigin");
    expect(q).toContain("sdp:exhibitMaterial");
    expect(q).toContain("sdp:exhibitHighlight");
  });

  it("menarik properti kedalaman pada kueri galeri", () => {
    const q = museumImagesQuery("museum-uji");
    expect(q).toContain("sdp:imagePeriod");
    expect(q).toContain("sdp:imageDetail");
  });

  it("memetakan metadata pameran dari baris SPARQL", () => {
    const exhibit = mapExhibitRow({
      title: { type: "literal", value: "Lonceng" },
      description: { type: "literal", value: "Deskripsi." },
      period: { type: "literal", value: "abad ke-15" },
      origin: { type: "literal", value: "Pasai" },
      material: { type: "literal", value: "perunggu" },
      highlight: { type: "literal", value: "true" },
    });
    expect(exhibit.period).toBe("abad ke-15");
    expect(exhibit.origin).toBe("Pasai");
    expect(exhibit.material).toBe("perunggu");
    expect(exhibit.highlight).toBe(true);
  });

  it("memetakan highlight dari boolean asli maupun string kosong", () => {
    const dariBoolean = mapExhibitRow({
      title: { type: "literal", value: "A" },
      highlight: { type: "literal", datatype: "xsd:boolean", value: "true" },
    });
    expect(dariBoolean.highlight).toBe(true);

    const tanpaHighlight = mapExhibitRow({ title: { type: "literal", value: "A" } });
    expect(tanpaHighlight.highlight).toBe(false);
  });

  it("mengumpulkan poin detail per foto menjadi array", () => {
    const images = mapGalleryRows([
      {
        index: { type: "literal", value: "1" },
        src: { type: "literal", value: "/a.jpg" },
        detail: { type: "literal", value: "Poin pertama" },
        period: { type: "literal", value: "1915" },
        sourceUrl: { type: "literal", value: "https://x" },
      },
      {
        index: { type: "literal", value: "1" },
        src: { type: "literal", value: "/a.jpg" },
        detail: { type: "literal", value: "Poin kedua" },
        sourceUrl: { type: "literal", value: "https://x" },
      },
    ]);
    expect(images).toHaveLength(1);
    expect(images[0].detail).toEqual(["Poin pertama", "Poin kedua"]);
    expect(images[0].period).toBe("1915");
  });
  it("memisahkan foto yang tidak punya index alih-alih menggabungkannya", () => {
    const images = mapGalleryRows([
      { src: { type: "literal", value: "/a.jpg" }, sourceUrl: { type: "literal", value: "https://a" } },
      { src: { type: "literal", value: "/b.jpg" }, sourceUrl: { type: "literal", value: "https://b" } },
    ]);
    expect(images.map((i) => i.src)).toEqual(["/a.jpg", "/b.jpg"]);
  });

  it("menggabungkan foto dengan index sama menjadi satu entri", () => {
    const images = mapGalleryRows([
      {
        index: { type: "literal", value: "1" },
        src: { type: "literal", value: "/a.jpg" },
        detail: { type: "literal", value: "Poin A" },
        sourceUrl: { type: "literal", value: "https://a" },
      },
      {
        index: { type: "literal", value: "1" },
        src: { type: "literal", value: "/a.jpg" },
        detail: { type: "literal", value: "Poin B" },
        sourceUrl: { type: "literal", value: "https://a" },
      },
    ]);
    expect(images).toHaveLength(1);
    expect(images[0].detail).toEqual(["Poin A", "Poin B"]);
  });
});

describe("loadRowsOrNull: membedakan error dari kosong", () => {
  const map = (b: SparqlBinding) => b.x?.value ?? null;
  it("mengembalikan array (boleh kosong) bila kueri berhasil", async () => {
    await expect(loadRowsOrNull("q", map, () => [])).resolves.toEqual([]);
    await expect(
      loadRowsOrNull("q", map, () => [{ x: { type: "literal", value: "a" } }]),
    ).resolves.toEqual(["a"]);
  });
  it("mengembalikan null bila kueri gagal", async () => {
    await expect(
      loadRowsOrNull("q", map, () => {
        throw new Error("offline");
      }),
    ).resolves.toBeNull();
  });
});
