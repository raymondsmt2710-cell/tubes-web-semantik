import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { buildRdf, escapeXml, RES } from "../src/lib/ontology";
import type { MuseumRecord } from "../src/lib/types";

const museumsPath = fileURLToPath(new URL("../data/museums.json", import.meta.url));
const museums = JSON.parse(readFileSync(museumsPath, "utf-8")) as MuseumRecord[];

const base: MuseumRecord = {
  slug: "museum-uji",
  name: "Museum Uji",
  city: "Kota Uji",
  province: "Aceh",
  themes: ["etnografi"],
  era: "kolonial",
  establishedYear: 1930,
  address: "Jl. Uji",
  latitude: 5.5,
  longitude: 95.3,
  description: "Deskripsi uji.",
  imageUrl: null,
  officialUrl: null,
  admissionNote: null,
  chapter: 1,
  verificationStatus: "perlu-verifikasi",
};

const countOf = (haystack: string, needle: string) => haystack.split(needle).length - 1;

describe("buildRdf", () => {
  it("menghasilkan RDF/XML dengan root rdf:RDF", () => {
    const xml = buildRdf(museums);
    expect(xml.startsWith('<?xml version="1.0" encoding="UTF-8"?>')).toBe(true);
    expect(xml).toContain("<rdf:RDF");
    expect(xml.trimEnd().endsWith("</rdf:RDF>")).toBe(true);
  });

  it("menulis tepat satu sdp:Museum per entri data", () => {
    const xml = buildRdf(museums);
    expect(countOf(xml, "<sdp:Museum ")).toBe(museums.length);
    expect(museums.length).toBe(28);
  });

  it("meng-escape karakter XML berbahaya", () => {
    const xml = buildRdf([{ ...base, name: 'Museum "A" & <B>' }]);
    expect(xml).toContain("&quot;A&quot; &amp; &lt;B&gt;");
    expect(xml).not.toContain("<B>");
  });

  it("menolak slug duplikat dan menyebut slug yang bentrok", () => {
    expect(() => buildRdf([base, { ...base }])).toThrow(/museum-uji/);
  });

  it("menolak museum tanpa provinsi", () => {
    expect(() => buildRdf([{ ...base, province: "" }])).toThrow(/provinsi/i);
  });

  it("menolak provinsi di luar daftar resmi", () => {
    expect(() => buildRdf([{ ...base, province: "Jawa Barat" }])).toThrow(/provinsi/i);
  });

  it("menolak museum tanpa tema", () => {
    expect(() => buildRdf([{ ...base, themes: [] }])).toThrow(/tema/i);
  });

  it("menolak bab di luar rentang 1..7", () => {
    expect(() => buildRdf([{ ...base, chapter: 9 }])).toThrow(/bab/i);
  });

  it("menulis establishedYear sebagai xsd:gYear hanya bila terisi", () => {
    const withYear = buildRdf([base]);
    expect(withYear).toContain('rdf:datatype="http://www.w3.org/2001/XMLSchema#gYear">1930<');

    const withoutYear = buildRdf([{ ...base, establishedYear: null }]);
    // Ontologi tetap mendeklarasikan range xsd:gYear; yang tidak boleh muncul
    // adalah literal bertipe gYear pada instance museum.
    expect(withoutYear).not.toContain('#gYear">');
  });

  it("menulis satu rdf:resource per tema (multi-nilai)", () => {
    const xml = buildRdf([{ ...base, themes: ["etnografi", "perjuangan"] }]);
    expect(countOf(xml, "<sdp:hasTheme ")).toBe(2);
    expect(xml).toContain(`${RES}theme/etnografi`);
    expect(xml).toContain(`${RES}theme/perjuangan`);
  });

  it("menautkan museum ke resource provinsi, kota, era, dan bab", () => {
    const xml = buildRdf([base]);
    expect(xml).toContain(`<sdp:locatedInProvince rdf:resource="${RES}province/aceh"/>`);
    expect(xml).toContain(`<sdp:locatedInCity rdf:resource="${RES}city/kota-uji"/>`);
    expect(xml).toContain(`<sdp:hasEra rdf:resource="${RES}era/kolonial"/>`);
    expect(xml).toContain(`<sdp:chapter rdf:resource="${RES}chapter/1"/>`);
  });

  it("mendeklarasikan kelas dan properti ontologi", () => {
    const xml = buildRdf([base]);
    for (const cls of ["Museum", "Province", "City", "Theme", "Era", "Chapter"]) {
      expect(xml).toContain(`#${cls}">`);
    }
    for (const prop of [
      "locatedInProvince",
      "locatedInCity",
      "hasTheme",
      "hasEra",
      "chapter",
      "establishedYear",
      "verificationStatus",
      "chapterIndex",
    ]) {
      expect(xml).toContain(`#${prop}">`);
    }
  });
});

describe("escapeXml", () => {
  it("meng-escape lima entitas XML", () => {
    expect(escapeXml(`& < > " '`)).toBe("&amp; &lt; &gt; &quot; &apos;");
  });
});
