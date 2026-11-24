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
  it("mengembalikan seluruh 28 museum tanpa filter", () => {
    expect(search({})).toHaveLength(28);
  });

  it("menyaring provinsi Aceh menjadi 4 museum", () => {
    expect(search({ province: "Aceh" })).toHaveLength(4);
  });

  it("menyaring tema etnografi menjadi 15 museum", () => {
    expect(search({ theme: "etnografi" })).toHaveLength(15);
  });

  it("menyaring era kolonial menjadi 12 museum", () => {
    expect(search({ era: "kolonial" })).toHaveLength(12);
  });

  it("menyaring tahun minimum 1900 menjadi 13 museum", () => {
    expect(search({ minYear: 1900 })).toHaveLength(13);
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
    expect(results[0].establishedYear).toBe(2009);
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
    expect(candidates).toHaveLength(27);
    expect(candidates.some((m) => m.slug === "museum-negeri-aceh")).toBe(false);
  });

  it("mengembalikan museum per bab sesuai jumlah di sampul", () => {
    const counts = [1, 2, 3, 4, 5, 6, 7].map(
      (chapter) => rows(museumsByChapterQuery(chapter)).length,
    );
    expect(counts).toEqual([4, 5, 4, 4, 4, 4, 3]);
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
