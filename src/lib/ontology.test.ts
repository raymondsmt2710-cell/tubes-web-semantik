import { describe, it, expect } from "vitest";
import { buildRdf } from "./ontology";
import type { MuseumRecord } from "./types";

const record: MuseumRecord = {
  slug: "museum-uji",
  name: "Museum Uji",
  city: "Banda Aceh",
  province: "Aceh",
  themes: ["etnografi"],
  era: "kolonial",
  establishedYear: 1915,
  address: "Jl. Uji",
  latitude: 5.5,
  longitude: 95.3,
  description: "Deskripsi.",
  imageUrl: null,
  officialUrl: null,
  admissionNote: null,
  chapter: 1,
  verificationStatus: "perlu-verifikasi",
  exhibits: [
    {
      title: "Lonceng",
      description: "Deskripsi panjang.",
      period: "abad ke-15",
      origin: "Kesultanan Pasai",
      material: "perunggu",
      highlight: true,
    },
  ],
  gallery: [
    {
      src: "/images/museums/museum-uji/1.jpg",
      alt: "Foto",
      caption: "Keterangan",
      credit: "Seseorang",
      license: "CC BY-SA 4.0",
      licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
      sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
      period: "1915",
      detail: ["Poin pertama", "Poin kedua"],
    },
  ],
};

describe("buildRdf — kedalaman isi pameran dan foto", () => {
  it("menulis properti kedalaman pada Exhibit", () => {
    const xml = buildRdf([record]);
    expect(xml).toContain('<sdp:exhibitPeriod xml:lang="id">abad ke-15</sdp:exhibitPeriod>');
    expect(xml).toContain(
      '<sdp:exhibitOrigin xml:lang="id">Kesultanan Pasai</sdp:exhibitOrigin>',
    );
    expect(xml).toContain('<sdp:exhibitMaterial xml:lang="id">perunggu</sdp:exhibitMaterial>');
    expect(xml).toContain(
      '<sdp:exhibitHighlight rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</sdp:exhibitHighlight>',
    );
  });

  it("menulis properti kedalaman pada Image", () => {
    const xml = buildRdf([record]);
    expect(xml).toContain('<sdp:imagePeriod xml:lang="id">1915</sdp:imagePeriod>');
  });

  it("menulis satu triple imageDetail per poin", () => {
    const xml = buildRdf([record]);
    const matches = xml.match(/<sdp:imageDetail xml:lang="id">/g) ?? [];
    expect(matches).toHaveLength(2);
  });

  it("tidak menulis properti kedalaman bila bidang kosong", () => {
    const minimal: MuseumRecord = {
      ...record,
      exhibits: [{ title: "Lonceng", description: "Deskripsi." }],
      gallery: [],
    };
    const xml = buildRdf([minimal]);
    expect(xml).not.toContain("sdp:exhibitPeriod");
    expect(xml).not.toContain("sdp:exhibitHighlight");
  });

  it("mendeklarasikan properti baru dengan range XSD yang valid", () => {
    const xml = buildRdf([record]);
    expect(xml).toContain('rdf:about="https://museumsumatera.id/ontology#exhibitHighlight"');
    expect(xml).not.toContain("undefined#");
    expect(xml).toContain('<rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#boolean"/>');
  });
});
