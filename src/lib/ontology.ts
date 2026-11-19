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

function objectProperty(name: string, domain: string, range: string, label: string): string[] {
  return [
    `${INDENT}<owl:ObjectProperty rdf:about="${SDP}${name}">`,
    `${INDENT}    <rdfs:label xml:lang="id">${label}</rdfs:label>`,
    `${INDENT}    <rdfs:domain rdf:resource="${SDP}${domain}"/>`,
    `${INDENT}    <rdfs:range rdf:resource="${SDP}${range}"/>`,
    `${INDENT}</owl:ObjectProperty>`,
    "",
  ];
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

/**
 * Validasi yang gagal keras SEBELUM satu byte RDF ditulis. Data rusak yang
 * masuk ke Fuseki akan membuat seluruh situs tampak kosong, jadi lebih baik
 * generator berhenti dengan pesan yang menyebut baris mana yang salah.
 */
export function validateRecords(records: MuseumRecord[]): void {
  const seen = new Set<string>();

  for (const record of records) {
    if (!record.slug) {
      throw new Error(`Museum "${record.name ?? "(tanpa nama)"}" tidak punya slug.`);
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
  lines.push(...objectProperty("chapter", "Museum", "Chapter", "berada di bab"));

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
  const cities = new Map<string, string>();
  for (const record of records) {
    if (record.city) cities.set(toSlug(record.city), record.city);
  }
  lines.push("    <!-- Instance kota -->");
  lines.push("");
  for (const [slug, city] of cities) {
    lines.push(`${INDENT}<sdp:City rdf:about="${RES}city/${slug}">`);
    lines.push(`${INDENT}    <rdfs:label xml:lang="id">${escapeXml(city)}</rdfs:label>`);
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
    lines.push(`${INDENT}    <rdfs:comment xml:lang="id">${escapeXml(chapter.title)}</rdfs:comment>`);
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
    if (record.imageUrl) {
      lines.push(
        `${INDENT}    <sdp:imageUrl rdf:datatype="${XSD}anyURI">${escapeXml(record.imageUrl)}</sdp:imageUrl>`,
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
  }

  lines.push("</rdf:RDF>");
  return lines.join("\n");
}
