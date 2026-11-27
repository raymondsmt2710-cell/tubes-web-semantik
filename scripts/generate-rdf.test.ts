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
    // Data boleh bertambah; yang dijaga hanya agar tidak ada museum yang hilang.
    expect(museums.length).toBeGreaterThanOrEqual(28);
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

  it("menautkan kota ke provinsinya dan menulis judul bab", () => {
    const xml = buildRdf([base]);
    expect(xml).toContain(`<sdp:partOfProvince rdf:resource="${RES}province/aceh"/>`);
    expect(xml).toContain(
      '<sdp:chapterTitle xml:lang="id">Dari Pelabuhan ke Pedalaman</sdp:chapterTitle>',
    );
  });

  it("menolak satu kota yang tercatat di dua provinsi", () => {
    expect(() =>
      buildRdf([
        base,
        { ...base, slug: "museum-lain", province: "Sumatera Utara" },
      ]),
    ).toThrow(/Kota Uji/);
  });

  it("mendeklarasikan kelas dan properti ontologi", () => {
    const xml = buildRdf([base]);
    for (const cls of ["Museum", "Province", "City", "Theme", "Era", "Chapter", "Collection"]) {
      expect(xml).toContain(`#${cls}">`);
    }
    for (const prop of [
      "locatedInProvince",
      "locatedInCity",
      "partOfProvince",
      "hasTheme",
      "hasEra",
      "hasCollection",
      "chapter",
      "establishedYear",
      "verificationStatus",
      "chapterIndex",
      "chapterTitle",
    ]) {
      expect(xml).toContain(`#${prop}">`);
    }
  });
});

describe("ontology/museum-sumatera.ttl", () => {
  it("mendeklarasikan istilah yang dipakai generator dan kueri", () => {
    const ttl = readFileSync(
      fileURLToPath(new URL("../ontology/museum-sumatera.ttl", import.meta.url)),
      "utf-8",
    );

    for (const term of [
      "sdp:Museum",
      "sdp:Collection",
      "sdp:hasCollection",
      "sdp:chapterTitle",
      "sdp:partOfProvince",
      "sdp:chapterIndex",
    ]) {
      expect(ttl).toContain(term);
    }
  });
});

describe("buildRdf: sejarah, pameran, galeri, dan sumber", () => {
  const enriched: MuseumRecord = {
    ...base,
    history: ["Paragraf pertama.", "Paragraf kedua."],
    exhibits: [{ title: "Koleksi Uji", description: "Penjelasan koleksi uji." }],
    gallery: [
      {
        src: "/images/museums/museum-uji/1.jpg",
        alt: "Foto uji",
        caption: "Keterangan foto uji",
        credit: "Fotografer Uji",
        license: "CC BY-SA 4.0",
        licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0/",
        sourceUrl: "https://commons.wikimedia.org/wiki/File:Uji.jpg",
      },
    ],
    sources: [{ label: "Sumber Uji", url: "https://example.org/uji" }],
  };

  it("menggabungkan paragraf sejarah menjadi satu literal", () => {
    const xml = buildRdf([enriched]);
    expect(xml).toContain("Paragraf pertama.\n\nParagraf kedua.");
    expect(countOf(xml, "<sdp:history")).toBe(1);
  });

  it("menulis isi pameran sebagai subjek sdp:Exhibit berurutan", () => {
    const xml = buildRdf([enriched]);
    expect(xml).toContain(`<sdp:Exhibit rdf:about="${RES}museum/museum-uji/exhibit/1">`);
    expect(xml).toContain("Penjelasan koleksi uji.");
    expect(xml).toContain(`<sdp:hasExhibit rdf:resource="${RES}museum/museum-uji/exhibit/1"/>`);
  });

  it("menulis foto beserta kredit, lisensi, dan tautan sumber", () => {
    const xml = buildRdf([enriched]);
    expect(xml).toContain("<sdp:imageCredit");
    expect(xml).toContain("CC BY-SA 4.0");
    expect(xml).toContain("https://commons.wikimedia.org/wiki/File:Uji.jpg");
    expect(xml).toContain(`<sdp:hasImage rdf:resource="${RES}museum/museum-uji/image/1"/>`);
  });

  it("memakai foto galeri pertama sebagai gambar utama museum", () => {
    const xml = buildRdf([{ ...enriched, imageUrl: null }]);
    expect(xml).toContain(
      '<sdp:imageUrl rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">/images/museums/museum-uji/1.jpg</sdp:imageUrl>',
    );
  });

  it("menolak foto tanpa lisensi atau tautan sumber", () => {
    const broken = {
      ...enriched,
      gallery: [{ ...enriched.gallery![0], license: "", sourceUrl: "" }],
    };
    expect(() => buildRdf([broken])).toThrow(/foto ke-1/);
  });

  it("menolak sumber yang bukan URL http(s)", () => {
    expect(() =>
      buildRdf([{ ...enriched, sources: [{ label: "Uji", url: "bukan-url" }] }]),
    ).toThrow(/sumber ke-1/);
  });

  it("menulis latar belakang foto sehingga galeri tidak hanya berisi gambar", () => {
    const xml = buildRdf([
      {
        ...enriched,
        gallery: [
          {
            ...enriched.gallery![0],
            title: "Lonceng bersejarah",
            background: "Lonceng ini dipakai sebagai penanda kuasa kesultanan.",
          },
        ],
      },
    ]);
    expect(xml).toContain('>Lonceng bersejarah</sdp:imageTitle>');
    expect(xml).toContain("penanda kuasa kesultanan");
  });

  it("setiap foto di data asli punya judul dan latar belakang", () => {
    for (const museum of museums) {
      for (const image of museum.gallery ?? []) {
        expect(image.title, `${museum.slug} ${image.src} tanpa judul`).toBeTruthy();
        expect(
          (image.background ?? "").length,
          `${museum.slug} ${image.src} latar belakang terlalu pendek`,
        ).toBeGreaterThan(80);
      }
    }
  });

  it("setiap museum di data asli punya sejarah, isi pameran, dan sumber", () => {
    for (const museum of museums) {
      expect(museum.history?.length, `${museum.slug} tanpa sejarah`).toBeGreaterThan(0);
      expect(museum.exhibits?.length, `${museum.slug} tanpa isi pameran`).toBeGreaterThan(0);
      expect(museum.sources?.length, `${museum.slug} tanpa sumber`).toBeGreaterThan(0);
      for (const image of museum.gallery ?? []) {
        expect(image.license, `${museum.slug} foto tanpa lisensi`).toBeTruthy();
        expect(image.sourceUrl, `${museum.slug} foto tanpa sumber`).toMatch(/^https:\/\//);
      }
    }
  });
});

describe("buildRdf: konsistensi ontologi (aturan #1)", () => {
  it("properti ber-owl:inverseOf tidak menyimpan rdfs:domain/range eksplisit", () => {
    const xml = buildRdf([base]);
    // Ambil tiap blok owl:ObjectProperty, pastikan yang punya owl:inverseOf
    // tidak membawa rdfs:domain/rdfs:range.
    const blocks = xml.split("<owl:ObjectProperty").slice(1);
    for (const block of blocks) {
      const body = block.split("</owl:ObjectProperty>")[0];
      if (body.includes("owl:inverseOf")) {
        expect(body, `blok inverse membawa domain/range: ${body.slice(0, 80)}`).not.toContain(
          "rdfs:domain",
        );
        expect(body).not.toContain("rdfs:range");
      }
    }
  });

  it("tidak mendeklarasikan properti yang sama dua kali", () => {
    const xml = buildRdf([base]);
    const declared = [...xml.matchAll(/owl:ObjectProperty rdf:about="([^"]+)"/g)].map(
      (m) => m[1],
    );
    const seen = new Set<string>();
    for (const iri of declared) {
      expect(seen.has(iri), `ganda: ${iri}`).toBe(false);
      seen.add(iri);
    }
  });

  it("setiap target owl:inverseOf dideklarasikan sebagai owl:ObjectProperty", () => {
    const xml = buildRdf([base]);
    const targets = [...xml.matchAll(/owl:inverseOf rdf:resource="([^"]+)"/g)].map(
      (m) => m[1],
    );
    for (const target of targets) {
      expect(xml, `target inverse tak dideklarasikan: ${target}`).toContain(
        `owl:ObjectProperty rdf:about="${target}"`,
      );
    }
  });

  it("heritageStatusOf dideklarasikan Functional", () => {
    const xml = buildRdf([base]);
    const block = xml.split("<owl:ObjectProperty").find((b) => b.includes("heritageStatusOf"));
    expect(block).toContain("FunctionalProperty");
  });
});

describe("escapeXml", () => {
  it("meng-escape lima entitas XML", () => {
    expect(escapeXml(`& < > " '`)).toBe("&amp; &lt; &gt; &quot; &apos;");
  });
});

describe("buildRdf: ontologi mendalam", () => {
  it("mendeklarasikan subkelas Museum & Person, inverse, dan restriction", () => {
    const xml = buildRdf([base]);
    expect(xml).toContain("#StateMuseum\">");
    expect(xml).toContain("#SiteMuseum\">");
    expect(xml).toContain("#PrivateMuseum\">");
    expect(xml).toContain("rdfs:subClassOf");
    expect(xml).toContain("owl:inverseOf");
    expect(xml).toContain("owl:Restriction");
    expect(xml).toContain("owl:onProperty");
  });

  it("menulis tipe turunan pada instance museum", () => {
    const xml = buildRdf([{ ...base, types: ["StateMuseum", "SiteMuseum"] }]);
    expect(xml).toContain(`/ontology#StateMuseum`);
    expect(xml).toContain(`/ontology#SiteMuseum`);
  });

  it("menulis relatedMuseum dua arah dari relatedSlugs", () => {
    const a: MuseumRecord = { ...base, slug: "museum-a", city: "Kota A", relatedSlugs: ["museum-b"] };
    const b: MuseumRecord = { ...base, slug: "museum-b", city: "Kota B" };
    const xml = buildRdf([a, b]);
    // a→b dan b→a
    expect(xml).toContain(`<sdp:relatedMuseum rdf:resource="${RES}museum/museum-b"/>`);
    expect(xml).toContain(`<sdp:relatedMuseum rdf:resource="${RES}museum/museum-a"/>`);
  });

  it("menulis Collection hanya bila data menyebut koleksi", () => {
    const withCol = buildRdf([{ ...base, collections: ["etnografika"] }]);
    expect(withCol).toContain(`<sdp:Collection rdf:about="${RES}museum/museum-uji/collection/1">`);
    expect(withCol).toContain("etnografika");

    const withoutCol = buildRdf([base]);
    expect(withoutCol).not.toContain("<sdp:Collection rdf:about=");
  });

  it("menulis collectionSize sebagai xsd:integer, bukan gYear", () => {
    const xml = buildRdf([{ ...base, collectionSize: 6038 }]);
    expect(xml).toContain(
      'rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">6038<',
    );
    expect(xml).not.toContain("#gYear\">6038");
  });
});
