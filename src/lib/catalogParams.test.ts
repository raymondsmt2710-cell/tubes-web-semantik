import { describe, it, expect } from "vitest";
import {
  buildCatalogQuery,
  hasActiveFilters,
  parseCatalogParams,
} from "./catalogParams";

describe("parseCatalogParams", () => {
  it("membaca semua filter dari query string", () => {
    const params = parseCatalogParams(
      new URLSearchParams(
        "q=aceh&province=Aceh&theme=etnografi&era=kolonial&minYear=1900&sort=year&order=desc",
      ),
    );

    expect(params).toEqual({
      q: "aceh",
      province: "Aceh",
      theme: "etnografi",
      era: "kolonial",
      minYear: 1900,
      sort: "year",
      order: "desc",
    });
  });

  it("memakai default nama menaik saat query string kosong", () => {
    expect(parseCatalogParams(new URLSearchParams())).toEqual({
      q: undefined,
      province: undefined,
      theme: undefined,
      era: undefined,
      minYear: undefined,
      sort: "name",
      order: "asc",
    });
  });

  it("mengabaikan sort dan order yang tidak dikenal", () => {
    const params = parseCatalogParams(
      new URLSearchParams("sort=harga&order=naik"),
    );
    expect(params.sort).toBe("name");
    expect(params.order).toBe("asc");
  });

  it("mengabaikan minYear yang bukan angka", () => {
    expect(
      parseCatalogParams(new URLSearchParams("minYear=abc")).minYear,
    ).toBeUndefined();
  });

  it("memangkas spasi dan membuang q yang kosong", () => {
    const params = parseCatalogParams(
      new URLSearchParams("q=%20%20&province=%20Aceh%20"),
    );
    expect(params.q).toBeUndefined();
    expect(params.province).toBe("Aceh");
  });
});

describe("buildCatalogQuery", () => {
  it("hanya menulis filter yang terisi", () => {
    expect(buildCatalogQuery({ province: "Aceh", sort: "name", order: "asc" })).toBe(
      "province=Aceh&sort=name&order=asc",
    );
  });

  it("meng-encode nilai dengan aman", () => {
    const query = buildCatalogQuery({ q: "seni & budaya", sort: "year" });
    expect(query).toContain("q=seni+%26+budaya");
    expect(query).toContain("sort=year");
  });

  it("bolak-balik dengan parseCatalogParams tanpa kehilangan nilai", () => {
    const original = {
      q: "museum aceh",
      province: "Aceh",
      theme: "etnografi",
      era: "kolonial",
      minYear: 1900,
      sort: "year" as const,
      order: "desc" as const,
    };
    expect(parseCatalogParams(new URLSearchParams(buildCatalogQuery(original)))).toEqual(
      original,
    );
  });
});

describe("hasActiveFilters", () => {
  it("false bila hanya berisi pengurutan", () => {
    expect(hasActiveFilters({ sort: "year", order: "desc" })).toBe(false);
  });

  it("true bila ada kata kunci atau filter penyaring", () => {
    expect(hasActiveFilters({ q: "aceh" })).toBe(true);
    expect(hasActiveFilters({ province: "Aceh" })).toBe(true);
    expect(hasActiveFilters({ theme: "etnografi" })).toBe(true);
    expect(hasActiveFilters({ era: "kolonial" })).toBe(true);
    expect(hasActiveFilters({ minYear: 1900 })).toBe(true);
  });
});
