import {
  ERAS,
  PROVINCES,
  THEMES,
  toSlug,
  type MuseumRecord,
} from "./types";
import { CHAPTERS } from "./chapters";

export const SDP = "https://museumsumatera.id/ontology#";
export const RES = "https://museumsumatera.id/resource/";
const RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";
const RDFS = "http://www.w3.org/2000/01/rdf-schema#";
const OWL = "http://www.w3.org/2002/07/owl#";
const XSD = "http://www.w3.org/2001/XMLSchema#";

export function escapeXml(value: string | null | undefined): string {
  if (!value) return "";
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

const INDENT = "    ";

function classBlock(name: string, label: string, comment: string): string[] {
  return [
    `${INDENT}<owl:Class rdf:about="${SDP}${name}">`,
    `${INDENT}    <rdfs:label xml:lang="id">${label}</rdfs:label>`,
    `${INDENT}    <rdfs:comment xml:lang="id">${comment}</rdfs:comment>`,
    `${INDENT}</owl:Class>`,
    "",
  ];
}

function objectProperty(
  name: string,
  domain: string,
  range: string,
  label: string,
  inverse?: string,
  extraTypes: string[] = [],
): string[] {
  const lines = [
    `${INDENT}<owl:ObjectProperty rdf:about="${SDP}${name}">`,
    `${INDENT}    <rdfs:label xml:lang="id">${label}</rdfs:label>`,
  ];
  for (const extra of extraTypes) {
    lines.push(`${INDENT}    <rdf:type rdf:resource="${extra}"/>`);
  }
  if (inverse) {
    // Properti yang punya owl:inverseOf tidak menyimpan domain/range eksplisit:
    // OWL 2 RL akan menyimpulkan kelas salah -> graf inconsistent.
    lines.push(`${INDENT}    <owl:inverseOf rdf:resource="${SDP}${inverse}"/>`);
  } else {
    lines.push(`${INDENT}    <rdfs:domain rdf:resource="${SDP}${domain}"/>`);
    lines.push(`${INDENT}    <rdfs:range rdf:resource="${SDP}${range}"/>`);
  }
  lines.push(`${INDENT}</owl:ObjectProperty>`, "");
  return lines;
}

function datatypeProperty(
  name: string,
  domain: string,
  range: string,
  label: string,
): string[] {
  return [
    `${INDENT}<owl:DatatypeProperty rdf:about="${SDP}${name}">`,
    `${INDENT}    <rdfs:label xml:lang="id">${label}</rdfs:label>`,
    `${INDENT}    <rdfs:domain rdf:resource="${SDP}${domain}"/>`,
    `${INDENT}    <rdfs:range rdf:resource="${range}"/>`,
    `${INDENT}</owl:DatatypeProperty>`,
    "",
  ];
}

interface CityInfo {
  label: string;
  provinceSlug: string;
}

/**
 * Mengumpulkan kota unik beserta provinsinya. Satu slug kota yang muncul di
 * dua provinsi berbeda adalah kesalahan data: relasi sdp:partOfProvince tidak
 * bisa menunjuk dua induk sekaligus.
 */
function collectCities(records: MuseumRecord[]): Map<string, CityInfo> {
  const cities = new Map<string, CityInfo>();

  for (const record of records) {
    if (!record.city) continue;
    const slug = toSlug(record.city);
    const provinceSlug = toSlug(record.province);
    const existing = cities.get(slug);

    if (existing && existing.provinceSlug !== provinceSlug) {
      throw new Error(
        `Kota "${record.city}" tercatat di lebih dari satu provinsi: "${existing.provinceSlug}" dan "${provinceSlug}".`,
      );
    }

    cities.set(slug, { label: record.city, provinceSlug });
  }

  return cities;
}

/**
 * Validasi yang gagal keras SEBELUM satu byte RDF ditulis. Data rusak yang
 * masuk ke Fuseki akan membuat seluruh situs tampak kosong, jadi lebih baik
 * generator berhenti dengan pesan yang menyebut baris mana yang salah.
 */
export function validateRecords(records: MuseumRecord[]): void {
  const seen = new Set<string>();
  collectCities(records);

  for (const record of records) {
    if (!record.slug) {
      throw new Error(`Museum "${record.name ?? "(tanpa nama)"}" tidak punya slug.`);
    }
    for (const [index, image] of (record.gallery ?? []).entries()) {
      if (!image.src || !image.sourceUrl || !image.license) {
        throw new Error(
          `Museum "${record.slug}" foto ke-${index + 1} harus punya src, sourceUrl, dan license.`,
        );
      }
    }
    for (const [index, source] of (record.sources ?? []).entries()) {
      if (!source.url?.startsWith("http")) {
        throw new Error(
          `Museum "${record.slug}" sumber ke-${index + 1} bukan URL http(s): "${source.url}".`,
        );
      }
    }
    if (seen.has(record.slug)) {
      throw new Error(`Slug duplikat: "${record.slug}". Setiap museum harus unik.`);
    }
    seen.add(record.slug);

    if (!record.name?.trim()) {
      throw new Error(`Museum "${record.slug}" tidak punya nama.`);
    }
    if (!record.province?.trim()) {
      throw new Error(`Museum "${record.slug}" tidak punya provinsi.`);
    }
    if (!(PROVINCES as readonly string[]).includes(record.province)) {
      throw new Error(
        `Museum "${record.slug}" memakai provinsi tidak dikenal: "${record.province}".`,
      );
    }
    if (!Array.isArray(record.themes) || record.themes.length === 0) {
      throw new Error(`Museum "${record.slug}" tidak punya tema.`);
    }
    for (const theme of record.themes) {
      if (!(THEMES as readonly string[]).includes(theme)) {
        throw new Error(`Museum "${record.slug}" memakai tema tidak dikenal: "${theme}".`);
      }
    }
    if (record.era && !(ERAS as readonly string[]).includes(record.era)) {
      throw new Error(`Museum "${record.slug}" memakai era tidak dikenal: "${record.era}".`);
    }
    if (
      !Number.isInteger(record.chapter) ||
      record.chapter < 1 ||
      record.chapter > CHAPTERS.length
    ) {
      throw new Error(
        `Museum "${record.slug}" punya nomor bab di luar rentang 1..${CHAPTERS.length}: ${record.chapter}.`,
      );
    }
  }
}

/**
 * Mengumpulkan semua museum terkait untuk satu museum, DUA ARAH. Untuk setiap
 * pasangan (A,B) di relatedSlugs, baik A maupun B mendapat relatedMuseum ke
 * pasangannya, supaya grafnya simetris walau Fuseki tidak memakai reasoner.
 */
function allRelatedFor(
  slug: string,
  records: MuseumRecord[],
  ownTargets: Set<string>,
): Set<string> {
  const result = new Set<string>(ownTargets);
  for (const record of records) {
    if (record.slug === slug) continue;
    if ((record.relatedSlugs ?? []).includes(slug)) result.add(record.slug);
  }
  return result;
}

export function buildRdf(records: MuseumRecord[]): string {
  validateRecords(records);
  const lines: string[] = [];
  lines.push('<?xml version="1.0" encoding="UTF-8"?>');
  lines.push("<rdf:RDF");
  lines.push(`    xmlns:rdf="${RDF}"`);
  lines.push(`    xmlns:rdfs="${RDFS}"`);
  lines.push(`    xmlns:owl="${OWL}"`);
  lines.push(`    xmlns:xsd="${XSD}"`);
  lines.push(`    xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"`);
  lines.push(`    xmlns:sdp="${SDP}"`);
  lines.push(`    xmlns:res="${RES}">`);
  lines.push("");

  lines.push("    <!-- Kelas -->");
  lines.push("");
  lines.push(...classBlock("Museum", "Museum", "Sebuah museum di Pulau Sumatera."));
  lines.push(...classBlock("Province", "Provinsi", "Provinsi di Pulau Sumatera."));
  lines.push(...classBlock("City", "Kota atau Kabupaten", "Lokasi kota atau kabupaten."));
  lines.push(...classBlock("Theme", "Tema", "Tema koleksi museum."));
  lines.push(...classBlock("Era", "Era", "Periode sejarah yang diwakili koleksi."));
  lines.push(...classBlock("Chapter", "Bab", "Bab dalam alur pameran."));
  lines.push(
    ...classBlock("Collection", "Koleksi", "Klasifikasi koleksi yang dimiliki museum."),
  );
  lines.push(
    ...classBlock("Exhibit", "Isi Pameran", "Bagian atau koleksi yang dipamerkan di museum."),
  );
  lines.push(
    ...classBlock("Image", "Gambar", "Foto museum atau koleksi beserta kredit dan lisensinya."),
  );
  lines.push(
    ...classBlock("Source", "Sumber", "Rujukan yang dipakai untuk menyusun catatan museum."),
  );
  lines.push(
    ...classBlock("StateMuseum", "Museum Negeri", "Museum yang dikelola pemerintah."),
  );
  lines.push(
    ...classBlock("SiteMuseum", "Museum Situs", "Museum situs/cagar atau bangunan bersejarah."),
  );
  lines.push(
    ...classBlock("PrivateMuseum", "Museum Swasta", "Museum milik yayasan atau perorangan."),
  );
  lines.push(...classBlock("Person", "Tokoh", "Orang yang terkait dengan museum."));
  lines.push(...classBlock("Founder", "Pendiri", "Tokoh pendiri museum."));
  lines.push(...classBlock("Curator", "Kurator", "Tokoh yang mengelola museum."));
  lines.push(...classBlock("Facility", "Fasilitas", "Fasilitas yang tersedia di museum."));
  lines.push(
    ...classBlock("HeritageStatus", "Status Cagar Budaya", "Status penetapan cagar budaya."),
  );

  // ---- Hierarki subClassOf ----
  lines.push("    <!-- Hierarki subkelas -->");
  lines.push("");
  const subclasses: [string, string, string?][] = [
    ["StateMuseum", "Museum", "PrivateMuseum"],
    ["SiteMuseum", "Museum"],
    ["PrivateMuseum", "Museum"],
    ["Founder", "Person"],
    ["Curator", "Person"],
  ];
  for (const [child, parent, disjointWith] of subclasses) {
    lines.push(`${INDENT}<owl:Class rdf:about="${SDP}${child}">`);
    lines.push(`${INDENT}    <rdfs:subClassOf rdf:resource="${SDP}${parent}"/>`);
    if (disjointWith) {
      lines.push(`${INDENT}    <owl:disjointWith rdf:resource="${SDP}${disjointWith}"/>`);
    }
    lines.push(`${INDENT}</owl:Class>`);
    lines.push("");
  }

  // ---- Restriction cardinality pada Museum ----
  const restriction = (property: string, kind: string, n: number): string[] => [
    `${INDENT}<rdfs:subClassOf>`,
    `${INDENT}    <owl:Restriction>`,
    `${INDENT}        <owl:onProperty rdf:resource="${SDP}${property}"/>`,
    `${INDENT}        <owl:${kind} rdf:datatype="${XSD}nonNegativeInteger">${n}</owl:${kind}>`,
    `${INDENT}    </owl:Restriction>`,
    `${INDENT}</rdfs:subClassOf>`,
  ];
  lines.push("    <!-- Restriction cardinality pada Museum -->");
  lines.push("");
  lines.push(`${INDENT}<owl:Class rdf:about="${SDP}Museum">`);
  lines.push(...restriction("locatedInProvince", "cardinality", 1));
  lines.push(...restriction("chapter", "cardinality", 1));
  lines.push(...restriction("hasTheme", "minCardinality", 1));
  lines.push(...restriction("locatedInCity", "maxCardinality", 1));
  lines.push(`${INDENT}</owl:Class>`);
  lines.push("");

  lines.push("    <!-- Object property -->");
  lines.push("");
  lines.push(
    ...objectProperty("locatedInProvince", "Museum", "Province", "berlokasi di provinsi"),
  );
  lines.push(...objectProperty("locatedInCity", "Museum", "City", "berlokasi di kota"));
  lines.push(
    ...objectProperty("partOfProvince", "City", "Province", "bagian dari provinsi"),
  );
  lines.push(...objectProperty("hasTheme", "Museum", "Theme", "memiliki tema"));
  lines.push(...objectProperty("hasEra", "Museum", "Era", "memiliki era"));
  lines.push(...objectProperty("hasExhibit", "Museum", "Exhibit", "memiliki isi pameran", "exhibitOfMuseum"));
  lines.push(...objectProperty("hasImage", "Museum", "Image", "memiliki foto", "imageOfMuseum"));
  lines.push(...objectProperty("hasSource", "Museum", "Source", "memiliki sumber acuan", "sourceOfMuseum"));
  lines.push(...objectProperty("chapter", "Museum", "Chapter", "berada di bab"));
  lines.push(
    ...objectProperty("hasCollection", "Museum", "Collection", "memiliki koleksi", "collectionOfMuseum"),
  );
  lines.push(
    ...objectProperty("hasFacility", "Museum", "Facility", "memiliki fasilitas", "facilityOfMuseum"),
  );
  lines.push(
    ...objectProperty("hasFounder", "Museum", "Person", "memiliki pendiri", "founderOfMuseum"),
  );
  lines.push(
    ...objectProperty("hasCurator", "Museum", "Person", "memiliki kurator"),
  );
  lines.push(
    ...objectProperty("namedAfter", "Museum", "Person", "dinamai menurut", "isNamesakeOfMuseum"),
  );
  lines.push(...objectProperty("heritageStatusOf", "Museum", "HeritageStatus", "status cagar budaya", "isHeritageStatusOf", ["http://www.w3.org/2002/07/owl#FunctionalProperty"]));
  // relatedMuseum simetris: generator menulis dua arah.
  lines.push(`${INDENT}<owl:ObjectProperty rdf:about="${SDP}relatedMuseum">`);
  lines.push(`${INDENT}    <rdfs:label xml:lang="id">museum terkait</rdfs:label>`);
  lines.push(`${INDENT}    <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#SymmetricProperty"/>`);
  lines.push(`${INDENT}    <rdfs:domain rdf:resource="${SDP}Museum"/>`);
  lines.push(`${INDENT}    <rdfs:range rdf:resource="${SDP}Museum"/>`);
  lines.push(`${INDENT}</owl:ObjectProperty>`);
  lines.push("");
  // Deklarasi eksplisit setiap properti inverse (kebalikan has*), supaya
  // owl:inverseOf menunjuk properti yang benar-benar bertipe ObjectProperty.
  const inversePairs: [string, string][] = [
    ["imageOfMuseum", "hasImage"],
    ["exhibitOfMuseum", "hasExhibit"],
    ["sourceOfMuseum", "hasSource"],
    ["collectionOfMuseum", "hasCollection"],
    ["facilityOfMuseum", "hasFacility"],
    ["founderOfMuseum", "hasFounder"],
    ["isNamesakeOfMuseum", "namedAfter"],
    ["isHeritageStatusOf", "heritageStatusOf"],
  ];
  for (const [inverseName, forward] of inversePairs) {
    lines.push(`${INDENT}<owl:ObjectProperty rdf:about="${SDP}${inverseName}">`);
    lines.push(`${INDENT}    <rdfs:label xml:lang="id">kebalikan ${forward}</rdfs:label>`);
    lines.push(`${INDENT}    <owl:inverseOf rdf:resource="${SDP}${forward}"/>`);
    lines.push(`${INDENT}</owl:ObjectProperty>`);
    lines.push("");
  }

  lines.push("    <!-- Datatype property -->");
  lines.push("");
  lines.push(
    ...datatypeProperty(
      "establishedYear",
      "Museum",
      `${XSD}gYear`,
      "tahun berdiri",
    ),
  );
  lines.push(
    ...datatypeProperty("description", "Museum", `${XSD}string`, "deskripsi"),
  );
  lines.push(...datatypeProperty("imageUrl", "Museum", `${XSD}anyURI`, "tautan gambar"));
  lines.push(
    ...datatypeProperty("officialUrl", "Museum", `${XSD}anyURI`, "situs resmi"),
  );
  lines.push(...datatypeProperty("address", "Museum", `${XSD}string`, "alamat"));
  lines.push(...datatypeProperty("latitude", "Museum", `${XSD}decimal`, "lintang"));
  lines.push(...datatypeProperty("longitude", "Museum", `${XSD}decimal`, "bujur"));
  lines.push(
    ...datatypeProperty("admissionNote", "Museum", `${XSD}string`, "catatan kunjungan"),
  );
  lines.push(...datatypeProperty("history", "Museum", `${XSD}string`, "sejarah museum"));
  lines.push(
    ...datatypeProperty("exhibitIndex", "Exhibit", `${XSD}integer`, "urutan isi pameran"),
  );
  lines.push(
    ...datatypeProperty("exhibitTitle", "Exhibit", `${XSD}string`, "judul isi pameran"),
  );
  lines.push(
    ...datatypeProperty(
      "exhibitDescription",
      "Exhibit",
      `${XSD}string`,
      "penjelasan isi pameran",
    ),
  );
  lines.push(
    ...datatypeProperty("exhibitPeriod", "Exhibit", `${XSD}string`, "masa atau tarikh benda"),
  );
  lines.push(...datatypeProperty("exhibitOrigin", "Exhibit", `${XSD}string`, "asal benda"));
  lines.push(...datatypeProperty("exhibitMaterial", "Exhibit", `${XSD}string`, "bahan benda"));
  lines.push(
    ...datatypeProperty("exhibitHighlight", "Exhibit", `${XSD}boolean`, "benda andalan"),
  );
  lines.push(...datatypeProperty("imageIndex", "Image", `${XSD}integer`, "urutan foto"));
  lines.push(...datatypeProperty("imageTitle", "Image", `${XSD}string`, "judul foto"));
  lines.push(
    ...datatypeProperty("imageBackground", "Image", `${XSD}string`, "latar belakang foto"),
  );
  lines.push(
    ...datatypeProperty("imagePeriod", "Image", `${XSD}string`, "masa atau tarikh foto"),
  );
  lines.push(
    ...datatypeProperty("imageDetail", "Image", `${XSD}string`, "poin pengamatan foto"),
  );
  lines.push(...datatypeProperty("imageAlt", "Image", `${XSD}string`, "teks alternatif foto"));
  lines.push(...datatypeProperty("imageCaption", "Image", `${XSD}string`, "keterangan foto"));
  lines.push(...datatypeProperty("imageCredit", "Image", `${XSD}string`, "kredit fotografer"));
  lines.push(...datatypeProperty("imageLicense", "Image", `${XSD}string`, "lisensi foto"));
  lines.push(
    ...datatypeProperty("imageLicenseUrl", "Image", `${XSD}anyURI`, "tautan lisensi"),
  );
  lines.push(
    ...datatypeProperty("imageSource", "Image", `${XSD}anyURI`, "tautan sumber foto"),
  );
  lines.push(
    ...datatypeProperty("sourceIndex", "Source", `${XSD}integer`, "urutan sumber"),
  );
  lines.push(...datatypeProperty("sourceLabel", "Source", `${XSD}string`, "judul sumber"));
  lines.push(...datatypeProperty("sourceUrl", "Source", `${XSD}anyURI`, "tautan sumber"));
  lines.push(
    ...datatypeProperty(
      "verificationStatus",
      "Museum",
      `${XSD}string`,
      "status verifikasi data",
    ),
  );
  lines.push(
    ...datatypeProperty("chapterIndex", "Chapter", `${XSD}integer`, "urutan bab"),
  );
  lines.push(
    ...datatypeProperty("chapterTitle", "Chapter", `${XSD}string`, "judul bab"),
  );
  lines.push(
    ...datatypeProperty("collectionSize", "Museum", `${XSD}integer`, "ukuran koleksi"),
  );
  lines.push(
    ...datatypeProperty("governingBody", "Museum", `${XSD}string`, "badan pengelola"),
  );
  lines.push(
    ...datatypeProperty("openingHours", "Museum", `${XSD}string`, "jam buka"),
  );
  lines.push(
    ...datatypeProperty("collectionCategory", "Collection", `${XSD}string`, "kategori koleksi"),
  );
  lines.push(
    ...datatypeProperty("facilityName", "Facility", `${XSD}string`, "nama fasilitas"),
  );
  lines.push(
    ...datatypeProperty("personName", "Person", `${XSD}string`, "nama tokoh"),
  );
  lines.push(
    ...datatypeProperty("heritageLabel", "HeritageStatus", `${XSD}string`, "label status cagar budaya"),
  );

  // ---- Instance provinsi ----
  const provinces = [...new Set(records.map((r) => r.province))].sort((a, b) =>
    a.localeCompare(b),
  );
  lines.push("    <!-- Instance provinsi -->");
  lines.push("");
  for (const province of provinces) {
    lines.push(`${INDENT}<sdp:Province rdf:about="${RES}province/${toSlug(province)}">`);
    lines.push(`${INDENT}    <rdfs:label xml:lang="id">${escapeXml(province)}</rdfs:label>`);
    lines.push(`${INDENT}</sdp:Province>`);
    lines.push("");
  }

  // ---- Instance kota ----
  // Satu kota hanya boleh berada di satu provinsi; collectCities() sudah
  // menolak data yang melanggar aturan itu sebelum sampai ke sini.
  const cities = collectCities(records);
  lines.push("    <!-- Instance kota -->");
  lines.push("");
  for (const [slug, city] of cities) {
    lines.push(`${INDENT}<sdp:City rdf:about="${RES}city/${slug}">`);
    lines.push(`${INDENT}    <rdfs:label xml:lang="id">${escapeXml(city.label)}</rdfs:label>`);
    lines.push(
      `${INDENT}    <sdp:partOfProvince rdf:resource="${RES}province/${city.provinceSlug}"/>`,
    );
    lines.push(`${INDENT}</sdp:City>`);
    lines.push("");
  }

  // ---- Instance tema ----
  lines.push("    <!-- Instance tema -->");
  lines.push("");
  for (const theme of THEMES) {
    lines.push(`${INDENT}<sdp:Theme rdf:about="${RES}theme/${theme}">`);
    lines.push(`${INDENT}    <rdfs:label xml:lang="id">${theme}</rdfs:label>`);
    lines.push(`${INDENT}</sdp:Theme>`);
    lines.push("");
  }

  // ---- Instance era ----
  lines.push("    <!-- Instance era -->");
  lines.push("");
  for (const era of ERAS) {
    lines.push(`${INDENT}<sdp:Era rdf:about="${RES}era/${era}">`);
    lines.push(`${INDENT}    <rdfs:label xml:lang="id">${era}</rdfs:label>`);
    lines.push(`${INDENT}</sdp:Era>`);
    lines.push("");
  }

  // ---- Instance bab ----
  lines.push("    <!-- Instance bab -->");
  lines.push("");
  for (const chapter of CHAPTERS) {
    lines.push(`${INDENT}<sdp:Chapter rdf:about="${RES}chapter/${chapter.index}">`);
    lines.push(`${INDENT}    <rdfs:label xml:lang="id">${chapter.label}</rdfs:label>`);
    lines.push(
      `${INDENT}    <sdp:chapterTitle xml:lang="id">${escapeXml(chapter.title)}</sdp:chapterTitle>`,
    );
    lines.push(
      `${INDENT}    <sdp:chapterIndex rdf:datatype="${XSD}integer">${chapter.index}</sdp:chapterIndex>`,
    );
    lines.push(`${INDENT}</sdp:Chapter>`);
    lines.push("");
  }

  // ---- Instance museum ----
  lines.push("    <!-- Instance museum -->");
  lines.push("");
  for (const record of records) {
    const subject = `${RES}museum/${record.slug}`;
    lines.push(`${INDENT}<sdp:Museum rdf:about="${subject}">`);
    lines.push(`${INDENT}    <rdfs:label xml:lang="id">${escapeXml(record.name)}</rdfs:label>`);
    lines.push(
      `${INDENT}    <sdp:description xml:lang="id">${escapeXml(record.description)}</sdp:description>`,
    );
    lines.push(
      `${INDENT}    <sdp:locatedInProvince rdf:resource="${RES}province/${toSlug(record.province)}"/>`,
    );
    if (record.city) {
      lines.push(
        `${INDENT}    <sdp:locatedInCity rdf:resource="${RES}city/${toSlug(record.city)}"/>`,
      );
    }
    lines.push(`${INDENT}    <sdp:chapter rdf:resource="${RES}chapter/${record.chapter}"/>`);
    for (const theme of record.themes) {
      lines.push(`${INDENT}    <sdp:hasTheme rdf:resource="${RES}theme/${theme}"/>`);
    }
    if (record.era) {
      lines.push(`${INDENT}    <sdp:hasEra rdf:resource="${RES}era/${record.era}"/>`);
    }
    if (record.establishedYear !== null && record.establishedYear !== undefined) {
      lines.push(
        `${INDENT}    <sdp:establishedYear rdf:datatype="${XSD}gYear">${record.establishedYear}</sdp:establishedYear>`,
      );
    }
    if (record.address) {
      lines.push(`${INDENT}    <sdp:address xml:lang="id">${escapeXml(record.address)}</sdp:address>`);
    }
    if (record.latitude !== null && record.latitude !== undefined) {
      lines.push(
        `${INDENT}    <sdp:latitude rdf:datatype="${XSD}decimal">${record.latitude}</sdp:latitude>`,
      );
    }
    if (record.longitude !== null && record.longitude !== undefined) {
      lines.push(
        `${INDENT}    <sdp:longitude rdf:datatype="${XSD}decimal">${record.longitude}</sdp:longitude>`,
      );
    }
    if (record.history && record.history.length > 0) {
      const paragraphs = record.history
        .map((paragraph) => paragraph.trim())
        .filter(Boolean)
        .join("\n\n");
      lines.push(
        `${INDENT}    <sdp:history xml:lang="id">${escapeXml(paragraphs)}</sdp:history>`,
      );
    }
    const gallery = record.gallery ?? [];
    for (const [index, image] of gallery.entries()) {
      lines.push(
        `${INDENT}    <sdp:hasImage rdf:resource="${RES}museum/${record.slug}/image/${index + 1}"/>`,
      );
    }
    for (const [index] of (record.exhibits ?? []).entries()) {
      lines.push(
        `${INDENT}    <sdp:hasExhibit rdf:resource="${RES}museum/${record.slug}/exhibit/${index + 1}"/>`,
      );
    }
    for (const [index] of (record.sources ?? []).entries()) {
      lines.push(
        `${INDENT}    <sdp:hasSource rdf:resource="${RES}museum/${record.slug}/source/${index + 1}"/>`,
      );
    }
    // Tipe turunan (StateMuseum/SiteMuseum/PrivateMuseum)
    for (const museumType of record.types ?? []) {
      lines.push(`${INDENT}    <rdf:type rdf:resource="${SDP}${museumType}"/>`);
    }
    // Tautan entitas pendukung
    for (const [index] of (record.collections ?? []).entries()) {
      lines.push(
        `${INDENT}    <sdp:hasCollection rdf:resource="${RES}museum/${record.slug}/collection/${index + 1}"/>`,
      );
    }
    for (const [index] of (record.facilities ?? []).entries()) {
      lines.push(
        `${INDENT}    <sdp:hasFacility rdf:resource="${RES}museum/${record.slug}/facility/${index + 1}"/>`,
      );
    }
    if (record.founder) {
      lines.push(
        `${INDENT}    <sdp:hasFounder rdf:resource="${RES}museum/${record.slug}/founder/1"/>`,
      );
    }
    // relatedMuseum dua arah (simetris)
    const relatedTargets = new Set<string>();
    for (const targetSlug of record.relatedSlugs ?? []) {
      if (targetSlug !== record.slug) relatedTargets.add(targetSlug);
    }
    for (const slug of allRelatedFor(record.slug, records, relatedTargets)) {
      lines.push(`${INDENT}    <sdp:relatedMuseum rdf:resource="${RES}museum/${slug}"/>`);
    }
    if (record.collectionSize !== null && record.collectionSize !== undefined) {
      lines.push(
        `${INDENT}    <sdp:collectionSize rdf:datatype="${XSD}integer">${record.collectionSize}</sdp:collectionSize>`,
      );
    }
    if (record.governingBody) {
      lines.push(
        `${INDENT}    <sdp:governingBody xml:lang="id">${escapeXml(record.governingBody)}</sdp:governingBody>`,
      );
    }
    if (record.openingHours) {
      lines.push(
        `${INDENT}    <sdp:openingHours xml:lang="id">${escapeXml(record.openingHours)}</sdp:openingHours>`,
      );
    }
    const heroImage = record.imageUrl ?? gallery[0]?.src ?? null;
    if (heroImage) {
      lines.push(
        `${INDENT}    <sdp:imageUrl rdf:datatype="${XSD}anyURI">${escapeXml(heroImage)}</sdp:imageUrl>`,
      );
    }
    if (record.officialUrl) {
      lines.push(
        `${INDENT}    <sdp:officialUrl rdf:datatype="${XSD}anyURI">${escapeXml(record.officialUrl)}</sdp:officialUrl>`,
      );
    }
    if (record.admissionNote) {
      lines.push(
        `${INDENT}    <sdp:admissionNote xml:lang="id">${escapeXml(record.admissionNote)}</sdp:admissionNote>`,
      );
    }
    lines.push(
      `${INDENT}    <sdp:verificationStatus>${record.verificationStatus}</sdp:verificationStatus>`,
    );
    lines.push(`${INDENT}</sdp:Museum>`);
    lines.push("");

    for (const [index, image] of (record.gallery ?? []).entries()) {
      lines.push(
        `${INDENT}<sdp:Image rdf:about="${RES}museum/${record.slug}/image/${index + 1}">`,
      );
      lines.push(
        `${INDENT}    <sdp:imageIndex rdf:datatype="${XSD}integer">${index + 1}</sdp:imageIndex>`,
      );
      const fields: [string, string | null, string | null][] = [
        ["imageUrl", image.src, `${XSD}anyURI`],
        ["imageTitle", image.title ?? null, null],
        ["imageBackground", image.background ?? null, null],
        ["imagePeriod", image.period ?? null, null],
        ["imageAlt", image.alt, null],
        ["imageCaption", image.caption, null],
        ["imageCredit", image.credit, null],
        ["imageLicense", image.license, null],
        ["imageLicenseUrl", image.licenseUrl, `${XSD}anyURI`],
        ["imageSource", image.sourceUrl, `${XSD}anyURI`],
      ];
      for (const [key, value, datatype] of fields) {
        if (!value) continue;
        const attr = datatype ? ` rdf:datatype="${datatype}"` : ' xml:lang="id"';
        lines.push(
          `${INDENT}    <sdp:${key}${attr}>${escapeXml(value)}</sdp:${key}>`,
        );
      }
      for (const point of image.detail ?? []) {
        lines.push(
          `${INDENT}    <sdp:imageDetail xml:lang="id">${escapeXml(point)}</sdp:imageDetail>`,
        );
      }
      lines.push(`${INDENT}</sdp:Image>`);
      lines.push("");
    }

    for (const [index, exhibit] of (record.exhibits ?? []).entries()) {
      lines.push(
        `${INDENT}<sdp:Exhibit rdf:about="${RES}museum/${record.slug}/exhibit/${index + 1}">`,
      );
      lines.push(
        `${INDENT}    <sdp:exhibitIndex rdf:datatype="${XSD}integer">${index + 1}</sdp:exhibitIndex>`,
      );
      lines.push(
        `${INDENT}    <sdp:exhibitTitle xml:lang="id">${escapeXml(exhibit.title)}</sdp:exhibitTitle>`,
      );
      if (exhibit.description) {
        lines.push(
          `${INDENT}    <sdp:exhibitDescription xml:lang="id">${escapeXml(exhibit.description)}</sdp:exhibitDescription>`,
        );
      }
      const exhibitFields: [string, string | null][] = [
        ["exhibitPeriod", exhibit.period ?? null],
        ["exhibitOrigin", exhibit.origin ?? null],
        ["exhibitMaterial", exhibit.material ?? null],
      ];
      for (const [key, value] of exhibitFields) {
        if (!value) continue;
        lines.push(`${INDENT}    <sdp:${key} xml:lang="id">${escapeXml(value)}</sdp:${key}>`);
      }
      if (exhibit.highlight) {
        lines.push(
          `${INDENT}    <sdp:exhibitHighlight rdf:datatype="${XSD}boolean">true</sdp:exhibitHighlight>`,
        );
      }
      lines.push(`${INDENT}</sdp:Exhibit>`);
      lines.push("");
    }

    for (const [index, source] of (record.sources ?? []).entries()) {
      lines.push(
        `${INDENT}<sdp:Source rdf:about="${RES}museum/${record.slug}/source/${index + 1}">`,
      );
      lines.push(
        `${INDENT}    <sdp:sourceIndex rdf:datatype="${XSD}integer">${index + 1}</sdp:sourceIndex>`,
      );
      lines.push(
        `${INDENT}    <sdp:sourceLabel xml:lang="id">${escapeXml(source.label)}</sdp:sourceLabel>`,
      );
      lines.push(
        `${INDENT}    <sdp:sourceUrl rdf:datatype="${XSD}anyURI">${escapeXml(source.url)}</sdp:sourceUrl>`,
      );
      lines.push(`${INDENT}</sdp:Source>`);
      lines.push("");
    }

    for (const [index, category] of (record.collections ?? []).entries()) {
      lines.push(
        `${INDENT}<sdp:Collection rdf:about="${RES}museum/${record.slug}/collection/${index + 1}">`,
      );
      lines.push(
        `${INDENT}    <sdp:collectionCategory xml:lang="id">${escapeXml(category)}</sdp:collectionCategory>`,
      );
      lines.push(`${INDENT}</sdp:Collection>`);
      lines.push("");
    }

    for (const [index, facility] of (record.facilities ?? []).entries()) {
      lines.push(
        `${INDENT}<sdp:Facility rdf:about="${RES}museum/${record.slug}/facility/${index + 1}">`,
      );
      lines.push(
        `${INDENT}    <sdp:facilityName xml:lang="id">${escapeXml(facility)}</sdp:facilityName>`,
      );
      lines.push(`${INDENT}</sdp:Facility>`);
      lines.push("");
    }

    if (record.founder) {
      lines.push(
        `${INDENT}<sdp:Founder rdf:about="${RES}museum/${record.slug}/founder/1">`,
      );
      lines.push(
        `${INDENT}    <sdp:personName xml:lang="id">${escapeXml(record.founder)}</sdp:personName>`,
      );
      lines.push(`${INDENT}</sdp:Founder>`);
      lines.push("");
    }
  }

  lines.push("</rdf:RDF>");
  return lines.join("\n");
}
