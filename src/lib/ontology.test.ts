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

  it("menulis setiap poin detail sebagai node tersendiri dengan indeks urutnya", () => {
    const xml = buildRdf([record]);
    const poin = xml.match(/<sdp:ImageDetail rdf:about="[^"]+">/g) ?? [];
    expect(poin).toHaveLength(2);
    expect(xml).toContain(
      '<sdp:detailIndex rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">1</sdp:detailIndex>',
    );
    expect(xml).toContain(
      '<sdp:detailIndex rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">2</sdp:detailIndex>',
    );
    expect(xml).toContain('<sdp:detailText xml:lang="id">Poin pertama</sdp:detailText>');
    expect(xml).toContain('<sdp:detailText xml:lang="id">Poin kedua</sdp:detailText>');
  });

  it("menautkan setiap poin ke fotonya lewat imageDetail", () => {
    const xml = buildRdf([record]);
    expect(xml).toContain(
      '<sdp:imageDetail rdf:resource="https://museumsumatera.id/resource/museum/museum-uji/image/1/detail/1"/>',
    );
    expect(xml).toContain(
      '<sdp:imageDetail rdf:resource="https://museumsumatera.id/resource/museum/museum-uji/image/1/detail/2"/>',
    );
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
