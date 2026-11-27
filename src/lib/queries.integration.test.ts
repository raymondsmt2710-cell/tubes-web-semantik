import { beforeAll, describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { Store } from "oxigraph";
import {
  attachMuseumDetail,
  chaptersQuery,
  mapMuseumRow,
  museumBySlugQuery,
  museumsByChapterQuery,
  relatedCandidatesQuery,
  searchCatalogQuery,
  type CatalogParams,
} from "./queries";
import type { MuseumDTO } from "./types";
import type { SparqlBinding } from "./sparql";

/**
 * Uji integrasi nyata: RDF hasil generate dimuat ke mesin SPARQL (Oxigraph)
 * lalu kueri aplikasi dieksekusi apa adanya. Uji string saja tidak akan
 * menangkap perbedaan literal berbahasa seperti "Aceh" vs "Aceh"@id.
 */

const rdfPath = fileURLToPath(new URL("../../data/museum-sumatera.rdf", import.meta.url));

// Angka harapan dihitung dari sumber kebenaran (data/museums.json), bukan ditulis
// mati: data bertambah dan dikoreksi (tugas A4, museum baru), dan angka mati
// membuat test gagal bukan karena kuerinya salah.
interface RecordSumber {
  slug: string;
  province: string;
  themes: string[];
  era: string | null;
  chapter: number;
  establishedYear: number | string | null;
}
const sumber = JSON.parse(
  readFileSync(fileURLToPath(new URL("../../data/museums.json", import.meta.url)), "utf8"),
) as RecordSumber[];
const tahun = (m: RecordSumber) =>
  Number.parseInt(String(m.establishedYear ?? "").slice(0, 4), 10);
const tahunData = sumber.map(tahun).filter((t) => Number.isFinite(t));

interface OxTerm {
  termType: string;
  value: string;
}

let store: Store;

beforeAll(() => {
  store = new Store();
  store.load(readFileSync(rdfPath, "utf-8"), {
    format: "application/rdf+xml",
  });
});

function rowToBinding(row: Map<string, OxTerm>): SparqlBinding {
  const binding: SparqlBinding = {};
  for (const [key, term] of row) {
    binding[key] = { type: term.termType, value: term.value };
  }
  return binding;
}

function rows(query: string): SparqlBinding[] {
  const result = store.query(query) as unknown as Map<string, OxTerm>[];
  return result.map(rowToBinding);
}

function search(params: CatalogParams): MuseumDTO[] {
  return rows(searchCatalogQuery(params)).map(mapMuseumRow);
}

describe("kueri katalog terhadap RDF asli", () => {
  it("mengembalikan seluruh museum tanpa filter", () => {
    expect(sumber.length).toBeGreaterThanOrEqual(28);
    expect(search({})).toHaveLength(sumber.length);
  });

  it("menyaring provinsi Aceh sesuai data sumber", () => {
    const harapan = sumber.filter((m) => m.province === "Aceh").length;
    expect(harapan).toBeGreaterThan(0);
    expect(search({ province: "Aceh" })).toHaveLength(harapan);
  });

  it("menyaring tema etnografi sesuai data sumber", () => {
    const harapan = sumber.filter((m) => m.themes.includes("etnografi")).length;
    expect(harapan).toBeGreaterThan(0);
    expect(search({ theme: "etnografi" })).toHaveLength(harapan);
  });

  it("menyaring era kolonial sesuai data sumber", () => {
    const harapan = sumber.filter((m) => m.era === "kolonial").length;
    expect(harapan).toBeGreaterThan(0);
    expect(search({ era: "kolonial" })).toHaveLength(harapan);
  });

  it("menyaring tahun minimum 1900 sesuai data sumber", () => {
    const harapan = tahunData.filter((t) => t >= 1900).length;
    expect(harapan).toBeGreaterThan(0);
    expect(search({ minYear: 1900 })).toHaveLength(harapan);
  });

  it("menggabungkan filter provinsi dan tema", () => {
    const results = search({ province: "Aceh", theme: "etnografi" });
    expect(results.map((m) => m.slug).sort()).toEqual([
      "museum-malikussaleh",
      "museum-negeri-aceh",
    ]);
  });

  it("mengurutkan tahun menaik dengan museum bertahun di depan", () => {
    const results = search({ sort: "year", order: "asc" });
    expect(results[0].establishedYear).toBe(1915);
    expect(results[0].slug).toBe("museum-negeri-aceh");
    expect(results[results.length - 1].establishedYear).toBeNull();
  });

  it("mengurutkan tahun menurun dari tahun terbaru", () => {
    const results = search({ sort: "year", order: "desc" });
    expect(results[0].establishedYear).toBe(Math.max(...tahunData));
  });
});

describe("kueri detail terhadap RDF asli", () => {
  it("menemukan museum berdasarkan slug", () => {
    const found = rows(museumBySlugQuery("museum-negeri-aceh")).map(mapMuseumRow);
    expect(found).toHaveLength(1);
    expect(found[0].name).toBe("Museum Negeri Aceh");
    expect(found[0].chapterTitle).toBe("Dari Pelabuhan ke Pedalaman");
    expect(found[0].themes).toHaveLength(2);
  });

  it("mengecualikan museum itu sendiri dari kandidat benang merah", () => {
    const candidates = rows(relatedCandidatesQuery("museum-negeri-aceh")).map(mapMuseumRow);
    expect(candidates).toHaveLength(sumber.length - 1);
    expect(candidates.some((m) => m.slug === "museum-negeri-aceh")).toBe(false);
  });

  it("mengembalikan museum per bab sesuai jumlah di sampul", () => {
    const counts = [1, 2, 3, 4, 5, 6, 7].map(
      (chapter) => rows(museumsByChapterQuery(chapter)).length,
    );
    const harapan = [1, 2, 3, 4, 5, 6, 7].map(
      (chapter) => sumber.filter((m) => m.chapter === chapter).length,
    );
    expect(counts).toEqual(harapan);
  });

  it("membaca sejarah museum sebagai paragraf terpisah", () => {
    const found = rows(museumBySlugQuery("museum-negeri-aceh")).map(mapMuseumRow);
    expect(found[0].history.length).toBeGreaterThanOrEqual(2);
    expect(found[0].history[0]).toMatch(/Paviliun Aceh/);
  });

  it("menarik isi pameran, galeri, dan sumber museum", async () => {
    const museum = await attachMuseumDetail(
      rows(museumBySlugQuery("museum-negeri-aceh")).map(mapMuseumRow)[0],
      rows,
    );

    expect(museum.exhibits.length).toBeGreaterThanOrEqual(3);
    expect(museum.exhibits[0].title).toMatch(/Rumoh Aceh/);

    expect(museum.gallery.length).toBeGreaterThanOrEqual(1);
    const photo = museum.gallery[0];
    expect(photo.src).toMatch(/^\/images\/museums\/museum-negeri-aceh\//);
    expect(photo.license).toBeTruthy();
    expect(photo.sourceUrl).toMatch(/^https:\/\/commons\.wikimedia\.org\//);

    expect(museum.sources.length).toBeGreaterThanOrEqual(1);
    expect(museum.sources[0].url).toMatch(/^https:\/\//);
  });

  it("menghitung jumlah museum per bab lewat agregasi", () => {
    const result = rows(chaptersQuery());
    const byIndex = new Map(
      result.map((row) => [
        Number(row.chapterIndex?.value),
        Number(row.museumCount?.value),
      ]),
    );
    expect([...byIndex.keys()].sort((a, b) => a - b)).toEqual([1, 2, 3, 4, 5, 6, 7]);
    expect(byIndex.get(1)).toBe(4);
    expect(byIndex.get(7)).toBe(3);
  });
});
