import { SDP, RES } from "./ontology";
import { sparqlString, type SparqlBinding } from "./sparql";

/**
 * NL2SPARQL di sisi server: pertanyaan bahasa Indonesia → query → jawaban.
 *
 * Alurnya mengikuti materi P13 (skema, contoh, validasi, verbalisasi). Dua
 * perbedaan sadar dibanding versi Python:
 *
 * - **Skema diambil dari graf lewat query**, bukan dari ontologi yang
 *   di-hardcode, karena Fuseki adalah sumber kebenaran.
 * - **Validasi bentuk dilakukan di sini** (tanpa parser SPARQL penuh), lalu
 *   properti yang dipakai diperiksa terhadap kosakata graf.
 *
 * Guard memeriksa bentuk query, **bukan** hak akses pengguna.
 */

export const MAX_LIMIT = 50;

const PREFIXES = `
PREFIX sdp:  <${SDP}>
PREFIX res:  <${RES}>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
`.trim();

/**
 * Pola "nama entitas".
 *
 * Ada dua jalur data yang sah di proyek ini dan keduanya pernah dipakai:
 * generator Python menulis `sdp:name`, sedangkan generator RDF/XML (yang
 * datanya dimuat ke Fuseki) menulis `rdfs:label`. Kueri harus menerima
 * keduanya, kalau tidak aplikasi tampak kosong hanya karena data dimuat dari
 * pipeline yang berbeda. Jalur alternatif `|` dipilih (bukan UNION) supaya
 * polanya tetap satu dan ringkas.
 */
const NAMA = "(sdp:name|rdfs:label)";

/** Properti object yang boleh dipakai query (dicerminkan oleh ontologi). */
const OBJECT_PROPERTIES = [
  "locatedInProvince",
  "locatedInCity",
  "partOfProvince",
  "hasTheme",
  "hasEra",
  "hasExhibit",
  "hasImage",
  "hasSource",
  "chapter",
  "relatedMuseum",
] as const;

/** Properti data yang boleh dipakai query. */
const DATA_PROPERTIES = [
  "name",
  "description",
  "history",
  "establishedYear",
  "address",
  "collectionSize",
  "openingHours",
  "governingBody",
  "exhibitTitle",
  "exhibitDescription",
  "exhibitPeriod",
  "exhibitOrigin",
  "exhibitMaterial",
  "imageTitle",
  "imageCaption",
] as const;

const KOSAKATA = new Set<string>([
  ...OBJECT_PROPERTIES.map((p) => `${SDP}${p}`),
  ...DATA_PROPERTIES.map((p) => `${SDP}${p}`),
]);

const KELAS = [
  "Museum",
  "StateMuseum",
  "SiteMuseum",
  "PrivateMuseum",
  "Province",
  "City",
  "Theme",
  "Era",
  "Chapter",
  "Exhibit",
  "Image",
  "Collection",
  "Facility",
] as const;

for (const k of KELAS) KOSAKATA.add(`${SDP}${k}`);

export interface AskJawaban {
  pertanyaan: string;
  query: string;
  lolos: boolean;
  pesan: string;
  jawaban: string;
  sumber: string[];
  baris: string[][];
}

export interface Entitas {
  iri: string;
  label: string;
  jenis: string;
}

export type SelectRunner = (query: string) => Promise<SparqlBinding[]>;

// ------------------------------------------------------------------ intent

type Jenis = "daftar" | "hitung" | "atribut";
type Topik = "museum" | "pameran" | "galeri" | "provinsi" | "kota";

interface Intent {
  jenis: Jenis;
  topik: Topik;
  atribut: string | null;
  kata: string[];
}

/** Batas kata: "era" tidak boleh cocok di dalam "berapa". */
function adaKata(teks: string, kunci: string): boolean {
  return new RegExp(
    `(?<!\\w)${kunci.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?!\\w)`,
  ).test(teks);
}

export function bacaIntent(pertanyaan: string): Intent {
  const teks = pertanyaan
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim()
    .replace(/[?.!]+$/, "");

  // Atribut: "berapa tahun X berdiri" bukan permintaan hitung.
  let atribut: string | null = null;
  if (/(?:tahun|kapan)\b.{0,60}?\b(?:berdiri|didirikan|diresmikan|berdirinya)/.test(teks)) {
    atribut = "establishedYear";
  } else if (adaKata(teks, "alamat")) {
    atribut = "address";
  } else if (/(?:ukuran|jumlah)\s+koleksi/.test(teks)) {
    atribut = "collectionSize";
  }

  const hitung =
    atribut === null &&
    ["berapa", "jumlah", "banyak", "hitung", "total"].some((k) => adaKata(teks, k));

  let topik: Topik = "museum";
  if (adaKata(teks, "pameran") || adaKata(teks, "koleksi")) topik = "pameran";
  else if (adaKata(teks, "galeri") || adaKata(teks, "foto")) topik = "galeri";
  else if (adaKata(teks, "provinsi")) topik = "provinsi";
  else if (adaKata(teks, "kota")) topik = "kota";

  const kata = teks
    .split(" ")
    .map((k) => k.replace(/[^a-z0-9-]/g, ""))
    .filter(Boolean);

  return {
    jenis: atribut ? "atribut" : hitung ? "hitung" : "daftar",
    topik,
    atribut,
    kata,
  };
}

// ------------------------------------------------------------ pencarian entitas

/**
 * Cari entitas yang namanya disebut di pertanyaan, lewat query ke Fuseki.
 *
 * Label terpanjang menang supaya "Museum Negeri Aceh" mengalahkan "Aceh".
 */
export async function cariEntitas(
  pertanyaan: string,
  run: SelectRunner,
): Promise<Entitas[]> {
  const teks = pertanyaan.toLowerCase();
  const query = `${PREFIXES}
SELECT ?e ?label ?jenis WHERE {
  VALUES (?kelas ?jenis) {
    (sdp:Museum "museum") (sdp:City "kota") (sdp:Province "provinsi")
    (sdp:Theme "tema") (sdp:Era "era")
  }
  ?e a ?kelas ; ${NAMA} ?label .
}
LIMIT 500`;

  const rows = await run(query);
  const calon = rows
    .map((row) => ({
      iri: row.e?.value ?? "",
      label: row.label?.value ?? "",
      jenis: row.jenis?.value ?? "",
    }))
    .filter(
      (row) => row.iri && row.label && teks.includes(row.label.toLowerCase()),
    );

  const bobotJenis: Record<string, number> = {
    museum: 0,
    kota: 1,
    provinsi: 2,
    tema: 3,
    era: 4,
  };
  calon.sort((a, b) => {
    if (b.label.length !== a.label.length) return b.label.length - a.label.length;
    return (bobotJenis[a.jenis] ?? 9) - (bobotJenis[b.jenis] ?? 9);
  });

  return calon.slice(0, 2);
}

// ------------------------------------------------------------------ perakitan

export function rakitQuery(intent: Intent, entitas: Entitas[]): string {
  const jangkar = entitas[0];

  if (intent.jenis === "atribut" && intent.atribut) {
    if (jangkar) {
      return `${PREFIXES}
SELECT ?nilai WHERE {
  <${jangkar.iri}> sdp:${intent.atribut} ?nilai .
}
LIMIT ${MAX_LIMIT}`;
    }
    return `${PREFIXES}
SELECT ?nama ?nilai WHERE {
  ?m a sdp:Museum ; ${NAMA} ?nama ; sdp:${intent.atribut} ?nilai .
}
ORDER BY LCASE(STR(?nama))
LIMIT ${MAX_LIMIT}`;
  }

  if (intent.jenis === "hitung") {
    const pola =
      intent.topik === "pameran"
        ? "?x a sdp:Exhibit ."
        : intent.topik === "galeri"
          ? "?x a sdp:Image ."
          : intent.topik === "provinsi"
            ? "?x a sdp:Province ."
            : "?x a sdp:Museum .";
    return `${PREFIXES}
SELECT (COUNT(DISTINCT ?x) AS ?jumlah) WHERE {
  ${pola}
}
LIMIT ${MAX_LIMIT}`;
  }

  if (intent.topik === "pameran") {
    const pola = jangkar
      ? `  <${jangkar.iri}> sdp:hasExhibit ?x .\n  ?x sdp:exhibitTitle ?judul .`
      : `  ?m a sdp:Museum ; sdp:hasExhibit ?x .\n  ?x sdp:exhibitTitle ?judul .`;
    return `${PREFIXES}
SELECT ?x ?judul WHERE {
${pola}
}
ORDER BY ?judul
LIMIT ${MAX_LIMIT}`;
  }

  if (intent.topik === "galeri") {
    const pola = jangkar
      ? `  <${jangkar.iri}> sdp:hasImage ?x .\n  ?x sdp:imageTitle ?judul .`
      : `  ?m a sdp:Museum ; sdp:hasImage ?x .\n  ?x sdp:imageTitle ?judul .`;
    return `${PREFIXES}
SELECT ?x ?judul WHERE {
${pola}
}
ORDER BY ?judul
LIMIT ${MAX_LIMIT}`;
  }

  // Daftar museum, dengan penyaring lokasi bila ada jangkar kota/provinsi.
  const saring: string[] = [];
  if (jangkar) {
    if (jangkar.jenis === "kota") {
      saring.push(`  ?museum sdp:locatedInCity <${jangkar.iri}> .`);
    } else if (jangkar.jenis === "provinsi") {
      // Museum bisa menunjuk provinsi langsung atau lewat kotanya (multi-hop).
      saring.push(
        `  ?museum (sdp:locatedInProvince|(sdp:locatedInCity/sdp:partOfProvince)) <${jangkar.iri}> .`,
      );
    }
  }

  const terpakai = new Set([
    "museum",
    "yang",
    "di",
    "ada",
    "apa",
    "saja",
    "semua",
    "kota",
    "provinsi",
    "berapa",
  ]);
  if (jangkar) {
    for (const k of jangkar.label.toLowerCase().split(" ")) terpakai.add(k);
  }

  for (const kata of intent.kata) {
    if (terpakai.has(kata) || kata.length < 3) continue;
    saring.push(`  FILTER(CONTAINS(LCASE(STR(?nama)), LCASE(${sparqlString(kata)})))`);
  }

  return `${PREFIXES}
SELECT DISTINCT ?museum ?nama ?kota ?provinsi ?tahun WHERE {
  ?museum a sdp:Museum ; ${NAMA} ?nama .
  OPTIONAL { ?museum sdp:locatedInCity ?kotaNode . ?kotaNode ${NAMA} ?kota }
  OPTIONAL { ?museum sdp:locatedInProvince ?provNode . ?provNode ${NAMA} ?provinsi }
  OPTIONAL { ?museum sdp:establishedYear ?tahun }
${saring.join("\n")}
}
ORDER BY LCASE(STR(?nama))
LIMIT ${MAX_LIMIT}`;
}

// --------------------------------------------------------------------- guard

/** Apakah query hanya memakai kosakata yang dikenal graf. */
function iriAsing(query: string): string[] {
  // Baris PREFIX harus dibuang dulu: <https://…ontology#> di sana adalah
  // deklarasi namespace, bukan IRI yang dipakai di dalam pola.
  const badan = query
    .split("\n")
    .filter((baris) => !/^\s*PREFIX\b/i.test(baris))
    .join("\n");

  const asing: string[] = [];
  for (const match of badan.matchAll(/<([^>\s]+)>/g)) {
    const iri = match[1];
    if (iri.startsWith(SDP) && !KOSAKATA.has(iri)) asing.push(iri);
  }
  for (const match of badan.matchAll(/\bsdp:([A-Za-z][\w-]*)/g)) {
    const nama = match[1];
    if (!KOSAKATA.has(`${SDP}${nama}`)) asing.push(`sdp:${nama}`);
  }
  return [...new Set(asing)];
}

export function periksa(query: string): { lolos: boolean; pesan: string } {
  const q = query.trim();
  if (!q) return { lolos: false, pesan: "query kosong" };

  // 1. Hanya SELECT.
  if (!/^\s*(?:PREFIX\s+[\s\S]*?\s)?SELECT\b/i.test(q)) {
    return { lolos: false, pesan: "hanya SELECT" };
  }
  if (/\b(?:DELETE|INSERT|DROP|CLEAR|LOAD|CREATE|CONSTRUCT|DESCRIBE)\b/i.test(q)) {
    return { lolos: false, pesan: "hanya SELECT" };
  }

  // 2. LIMIT wajib ada dan <= MAX_LIMIT.
  const limit = q.match(/\bLIMIT\s+(\d+)\b/i);
  if (!limit) return { lolos: false, pesan: `wajib LIMIT <= ${MAX_LIMIT}` };
  if (Number(limit[1]) > MAX_LIMIT) {
    return { lolos: false, pesan: `LIMIT ${limit[1]} melebihi batas ${MAX_LIMIT}` };
  }

  // 3. Kurung kurawal seimbang.
  const buka = (q.match(/{/g) ?? []).length;
  const tutup = (q.match(/}/g) ?? []).length;
  if (buka !== tutup) return { lolos: false, pesan: "kurung kurawal tidak seimbang" };

  // 4. Semua IRI dikenal.
  const asing = iriAsing(q);
  if (asing.length > 0) {
    return { lolos: false, pesan: `IRI tidak dikenal: ${asing.join(", ")}` };
  }

  return { lolos: true, pesan: "ok" };
}

// -------------------------------------------------------------- verbalisasi

const ATURAN =
  "Jawab HANYA dari data di bawah. Jika data tidak cukup, katakan tidak cukup. " +
  "Jangan menambah fakta dari ingatan Anda.";

function rangkai(intent: Intent, baris: SparqlBinding[]): string {
  if (intent.jenis === "hitung") {
    const nilai = baris[0]?.jumlah?.value ?? "0";
    const satuan =
      intent.topik === "pameran" ? "pameran" : intent.topik === "galeri" ? "foto" : "entitas";
    return `Ada ${nilai} ${satuan} yang tercatat di graf.`;
  }

  if (intent.jenis === "atribut") {
    const label = intent.atribut === "establishedYear" ? "Tahun berdiri" : "Nilai";
    const nilai = baris[0]?.nilai?.value ?? "-";
    return `${label} menurut graf: ${nilai}.`;
  }

  if (intent.topik === "pameran" || intent.topik === "galeri") {
    const judul = baris.map((b) => b.judul?.value).filter((v): v is string => Boolean(v));
    const tampil = judul.slice(0, 10);
    const sisa = judul.length - tampil.length;
    const teks = `Ditemukan ${judul.length} ${intent.topik}: ${tampil.join("; ")}`;
    return sisa > 0 ? `${teks}; dan ${sisa} lainnya.` : `${teks}.`;
  }

  if (baris.length === 1) {
    return `Ditemukan 1 museum: ${baris[0].nama?.value ?? "-"}.`;
  }
  const nama = baris.map((b) => b.nama?.value).filter((v): v is string => Boolean(v));
  const tampil = nama.slice(0, 10);
  const sisa = nama.length - tampil.length;
  const teks = `Ditemukan ${nama.length} museum: ${tampil.join("; ")}`;
  return sisa > 0 ? `${teks}; dan ${sisa} lainnya.` : `${teks}.`;
}

/**
 * Alur utuh: baca intent → cari entitas → rakit query → guard → jalankan →
 * susun jawaban ber-sumber.
 *
 * Hasil kosong **tidak** diserahkan ke model; sistem langsung menjawab "tidak
 * ditemukan di graf" (P13 bagian 21). Sumber ditempel oleh kode dari IRI yang
 * benar-benar muncul di hasil query.
 */
export async function askGraph(
  pertanyaan: string,
  run: SelectRunner,
): Promise<AskJawaban> {
  void ATURAN;

  const intent = bacaIntent(pertanyaan);

  if (!pertanyaan.trim()) {
    return {
      pertanyaan,
      query: "",
      lolos: false,
      pesan: "pertanyaan kosong",
      jawaban: "Tulis pertanyaan terlebih dahulu.",
      sumber: [],
      baris: [],
    };
  }

  const entitas = await cariEntitas(pertanyaan, run);
  const query = rakitQuery(intent, entitas);

  const cek = periksa(query);
  if (!cek.lolos) {
    return {
      pertanyaan,
      query,
      lolos: false,
      pesan: cek.pesan,
      jawaban: `Query ditolak (${cek.pesan}).`,
      sumber: [],
      baris: [],
    };
  }

  const rows = await run(query);
  if (rows.length === 0) {
    return {
      pertanyaan,
      query,
      lolos: true,
      pesan: "ok",
      jawaban: "Tidak ditemukan di graf.",
      sumber: [],
      baris: [],
    };
  }

  const baris = rows.map((row) => Object.values(row).map((v) => v?.value ?? ""));
  const sumber = [
    ...new Set(
      rows.flatMap((row) =>
        Object.values(row)
          .map((v) => v?.value ?? "")
          .filter((v) => v.startsWith(RES)),
      ),
    ),
  ].sort();

  // Hitungan/atribut tidak memuat IRI di hasilnya. Bila hasil kosong dari
  // sumber, pakai jangkar pertanyaan supaya jawaban tetap dapat ditelusuri.
  const sumberFinal =
    sumber.length > 0
      ? sumber
      : entitas.map((e) => e.iri).filter((iri) => iri.startsWith(RES));

  let jawaban = rangkai(intent, rows);
  if (sumberFinal.length > 0) {
    jawaban += `\nSumber: ${sumberFinal.slice(0, 8).join(", ")}`;
  }

  return {
    pertanyaan,
    query,
    lolos: true,
    pesan: "ok",
    jawaban,
    sumber: sumberFinal,
    baris,
  };
}
