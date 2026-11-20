import { sparqlString, runSelect, type SparqlBinding } from "./sparql";
import { SDP, RES } from "./ontology";
import type {
  Exhibit,
  MuseumDTO,
  MuseumImage,
  SourceRef,
  VerificationStatus,
} from "./types";

const PREFIXES = `
PREFIX sdp:  <${SDP}>
PREFIX res:  <${RES}>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX geo:  <http://www.w3.org/2003/01/geo/wgs84_pos#>
`.trim();

/** Batas kandidat yang boleh masuk ke pemeringkatan teks di JavaScript. */
export const SEARCH_LIMIT = 300;

export interface CatalogParams {
  q?: string;
  province?: string;
  theme?: string;
  era?: string;
  minYear?: number;
  sort?: "name" | "year";
  order?: "asc" | "desc";
  chapterIndex?: number;
}

const MUSEUM_PROJECTION = `
  ?museum
  ?name
  ?description
  ?history
  ?imageUrl
  ?officialUrl
  ?address
  ?lat
  ?lon
  ?admissionNote
  ?verification
  ?province
  ?city
  ?era
  ?year
  ?chapterIndex
  ?chapterTitle
  ?themes
`;

const MUSEUM_PATTERNS = `
  ?museum a sdp:Museum ;
          rdfs:label ?name .
  BIND(REPLACE(STR(?museum), "^.*/museum/", "") AS ?slug)

  {
    SELECT ?museum (GROUP_CONCAT(DISTINCT ?themeLabel; separator="|") AS ?themes)
    WHERE {
      ?museum sdp:hasTheme ?themeResource .
      ?themeResource rdfs:label ?themeLabel .
    }
    GROUP BY ?museum
  }

  OPTIONAL { ?museum sdp:description ?description . }
  OPTIONAL { ?museum sdp:history ?history . }
  OPTIONAL { ?museum sdp:imageUrl ?imageUrl . }
  OPTIONAL { ?museum sdp:officialUrl ?officialUrl . }
  OPTIONAL { ?museum sdp:address ?address . }
  OPTIONAL { ?museum sdp:admissionNote ?admissionNote . }
  OPTIONAL { ?museum sdp:verificationStatus ?verification . }

  OPTIONAL {
    ?museum sdp:locatedInProvince ?provinceResource .
    ?provinceResource rdfs:label ?province .
  }

  OPTIONAL {
    ?museum sdp:locatedInCity ?cityResource .
    ?cityResource rdfs:label ?city .
  }

  OPTIONAL {
    ?museum sdp:hasEra ?eraResource .
    ?eraResource rdfs:label ?era .
  }

  OPTIONAL {
    ?museum sdp:establishedYear ?yearLiteral .
    BIND(xsd:integer(STR(?yearLiteral)) AS ?year)
  }

  OPTIONAL {
    ?museum sdp:chapter ?chapterResource .
    ?chapterResource sdp:chapterIndex ?chapterIndex ;
                    sdp:chapterTitle ?chapterTitle .
  }

  OPTIONAL {
    ?museum sdp:latitude ?lat .
    ?museum sdp:longitude ?lon .
  }
`;

function orderClause(sort: CatalogParams["sort"], order: CatalogParams["order"]): string {
  const direction = order === "desc" ? "DESC" : "ASC";

  if (sort === "year") {
    // Museum tanpa tahun diletakkan di ujung, bukan di awal, untuk kedua arah.
    return `ORDER BY (BOUND(?year) = false) ${direction}(?year)`;
  }

  return `ORDER BY ${direction}(?name)`;
}

export function searchCatalogQuery(params: CatalogParams = {}): string {
  const filters: string[] = [];

  if (params.q && params.q.trim()) {
    // Setiap kata harus muncul di salah satu bidang. Perbandingan memakai
    // LCASE + COALESCE agar aman untuk literal berbahasa dan field kosong.
    for (const token of params.q.trim().split(/\s+/).filter(Boolean)) {
      const needle = sparqlString(token.toLowerCase());
      filters.push(
        `FILTER(
    CONTAINS(LCASE(STR(?name)), "${needle}") ||
    CONTAINS(LCASE(COALESCE(STR(?city), "")), "${needle}") ||
    CONTAINS(LCASE(COALESCE(STR(?province), "")), "${needle}") ||
    CONTAINS(LCASE(COALESCE(STR(?themes), "")), "${needle}") ||
    CONTAINS(LCASE(COALESCE(STR(?era), "")), "${needle}") ||
    CONTAINS(LCASE(COALESCE(STR(?description), "")), "${needle}")
  )`,
      );
    }
  }

  if (params.province && params.province.trim()) {
    // Label memakai xml:lang="id", sehingga "Aceh"@id tidak sama dengan "Aceh".
    filters.push(`FILTER(STR(?province) = "${sparqlString(params.province.trim())}")`);
  }

  if (params.theme && params.theme.trim()) {
    filters.push(
      `FILTER EXISTS {
    ?museum sdp:hasTheme ?themeFilterResource .
    ?themeFilterResource rdfs:label ?themeFilterLabel .
    FILTER(STR(?themeFilterLabel) = "${sparqlString(params.theme.trim())}")
  }`,
    );
  }

  if (params.era && params.era.trim()) {
    filters.push(`FILTER(STR(?era) = "${sparqlString(params.era.trim())}")`);
  }

  if (
    params.minYear !== undefined &&
    params.minYear !== null &&
    Number.isFinite(params.minYear)
  ) {
    filters.push(`FILTER(BOUND(?year) && ?year >= ${Math.trunc(params.minYear)})`);
  }

  if (params.chapterIndex !== undefined) {
    filters.push(`FILTER(?chapterIndex = ${Math.trunc(params.chapterIndex)})`);
  }

  return `${PREFIXES}

SELECT ${MUSEUM_PROJECTION}
WHERE {
${MUSEUM_PATTERNS}
${filters.join("\n")}
}
${orderClause(params.sort, params.order)}
LIMIT ${SEARCH_LIMIT}
`;
}

export function museumsByChapterQuery(chapterIndex: number): string {
  if (!Number.isInteger(chapterIndex) || chapterIndex < 1 || chapterIndex > 7) {
    throw new Error(`Nomor bab harus bilangan bulat 1..7, bukan ${chapterIndex}.`);
  }
  return searchCatalogQuery({ chapterIndex, sort: "name", order: "asc" });
}

export function chaptersQuery(): string {
  return `${PREFIXES}

SELECT ?chapterIndex (COUNT(?museum) AS ?museumCount)
WHERE {
  ?museum a sdp:Museum ;
          sdp:chapter ?chapter .
  ?chapter sdp:chapterIndex ?chapterIndex .
}
GROUP BY ?chapterIndex
ORDER BY ?chapterIndex
`;
}

export function museumBySlugQuery(slug: string): string {
  return `${PREFIXES}

SELECT ${MUSEUM_PROJECTION}
WHERE {
${MUSEUM_PATTERNS}
  FILTER(?slug = "${sparqlString(slug)}")
}
LIMIT 1
`;
}

export function relatedCandidatesQuery(slug: string, limit = 80): string {
  return `${PREFIXES}

SELECT ${MUSEUM_PROJECTION}
WHERE {
${MUSEUM_PATTERNS}
  FILTER(?slug != "${sparqlString(slug)}")
}
ORDER BY ASC(?name)
LIMIT ${Math.trunc(limit)}
`;
}

/**
 * Isi pameran, galeri, dan sumber disimpan sebagai subjek terpisah di graf.
 * Kueri rincian menariknya per museum supaya kueri katalog tetap ringan.
 * Path foto sudah ditulis lengkap sebagai datatype property, jadi tidak perlu
 * diturunkan dari URI.
 */
export function museumExhibitsQuery(slug: string): string {
  return `${PREFIXES}
SELECT ?index ?title ?description
WHERE {
  ${museumIri(slug)} sdp:hasExhibit ?node .
  ?node sdp:exhibitIndex ?index ;
        sdp:exhibitTitle ?title .
  OPTIONAL { ?node sdp:exhibitDescription ?description . }
}
ORDER BY ?index
`;
}

export function museumImagesQuery(slug: string): string {
  return `${PREFIXES}
SELECT ?index ?src ?alt ?caption ?credit ?license ?licenseUrl ?sourceUrl
WHERE {
  ${museumIri(slug)} sdp:hasImage ?node .
  ?node sdp:imageIndex ?index ;
        sdp:imageSource ?sourceUrl .
  OPTIONAL { ?node sdp:imageUrl ?src . }
  OPTIONAL { ?node sdp:imageAlt ?alt . }
  OPTIONAL { ?node sdp:imageCaption ?caption . }
  OPTIONAL { ?node sdp:imageCredit ?credit . }
  OPTIONAL { ?node sdp:imageLicense ?license . }
  OPTIONAL { ?node sdp:imageLicenseUrl ?licenseUrl . }
}
ORDER BY ?index
`;
}

export function museumSourcesQuery(slug: string): string {
  return `${PREFIXES}
SELECT ?index ?label ?url
WHERE {
  ${museumIri(slug)} sdp:hasSource ?node .
  ?node sdp:sourceIndex ?index ;
        sdp:sourceLabel ?label ;
        sdp:sourceUrl ?url .
}
ORDER BY ?index
`;
}

/**
 * IRI museum ditulis penuh, bukan prefixed name. Sebagian mesin SPARQL
 * (termasuk Oxigraph yang dipakai uji integrasi) menolak prefixed name di
 * posisi subjek, sedangkan IRI penuh diterima semua mesin.
 */
function museumIri(slug: string): string {
  return `<${RES}museum/${slug}>`;
}

function str(binding: SparqlBinding, key: string): string | null {
  const value = binding[key]?.value;
  return value === undefined || value === "" ? null : value;
}

function num(binding: SparqlBinding, key: string): number | null {
  const raw = str(binding, key);
  if (raw === null) return null;
  const parsed = Number(raw);
  return Number.isFinite(parsed) ? parsed : null;
}

export function mapMuseumRow(binding: SparqlBinding): MuseumDTO {
  const uri = str(binding, "museum") ?? "";
  const slug = str(binding, "slug") ?? uri.split("/museum/")[1] ?? "";
  const themesRaw = str(binding, "themes");

  return {
    uri,
    slug,
    name: str(binding, "name") ?? "(tanpa nama)",
    province: str(binding, "province"),
    city: str(binding, "city"),
    themes: themesRaw ? themesRaw.split("|").filter(Boolean) : [],
    era: str(binding, "era"),
    establishedYear: num(binding, "year"),
    description: str(binding, "description"),
    imageUrl: str(binding, "imageUrl"),
    officialUrl: str(binding, "officialUrl"),
    address: str(binding, "address"),
    latitude: num(binding, "lat"),
    longitude: num(binding, "lon"),
    admissionNote: str(binding, "admissionNote"),
    verificationStatus: (str(binding, "verification") ?? "perlu-verifikasi") as VerificationStatus,
    chapterIndex: num(binding, "chapterIndex"),
    chapterTitle: str(binding, "chapterTitle"),
    history: splitParagraphs(str(binding, "history")),
    exhibits: [],
    gallery: [],
    sources: [],
  };
}

/** Sejarah disimpan sebagai satu literal dengan paragraf dipisah baris kosong. */
function splitParagraphs(value: string | null): string[] {
  if (!value) return [];
  return value
    .split(/\n\s*\n/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);
}

export function mapExhibitRow(binding: SparqlBinding): Exhibit {
  return {
    title: str(binding, "title") ?? "Tanpa judul",
    description: str(binding, "description") ?? "",
  };
}

export function mapGalleryRow(binding: SparqlBinding): MuseumImage {
  return {
    src: str(binding, "src") ?? "",
    alt: str(binding, "alt") ?? "",
    caption: str(binding, "caption") ?? "",
    credit: str(binding, "credit") ?? "Tidak dicatat",
    license: str(binding, "license") ?? "Tidak dicatat",
    licenseUrl: str(binding, "licenseUrl"),
    sourceUrl: str(binding, "sourceUrl") ?? "",
  };
}

export function mapSourceRow(binding: SparqlBinding): SourceRef {
  return {
    label: str(binding, "label") ?? str(binding, "url") ?? "Sumber",
    url: str(binding, "url") ?? "",
  };
}

/**
 * Menjalankan SELECT lalu memetakan setiap baris. `rows` dapat diisi pemanggil
 * (mis. uji integrasi dengan mesin SPARQL lokal) supaya kueri yang dipakai di
 * sini tetap sama persis dengan yang dipakai halaman.
 */
export async function loadRows<T>(
  query: string,
  map: (binding: SparqlBinding) => T | null,
  rows?: (query: string) => SparqlBinding[],
): Promise<T[]> {
  try {
    const bindings = rows ? rows(query) : await runSelect(query);
    return bindings
      .map(map)
      .filter((item): item is T => item !== null && item !== undefined);
  } catch {
    return [];
  }
}

/**
 * Melengkapi museum dari kueri katalog dengan isi pameran, galeri, dan sumber.
 * Dipakai halaman detail; kueri katalog sendiri tidak menarik rincian ini.
 */
export async function attachMuseumDetail(
  museum: MuseumDTO,
  rows?: (query: string) => SparqlBinding[],
): Promise<MuseumDTO> {
  const [exhibits, gallery, sources] = await Promise.all([
    loadRows(museumExhibitsQuery(museum.slug), mapExhibitRow, rows),
    loadRows(
      museumImagesQuery(museum.slug),
      (row) => {
        const image = mapGalleryRow(row);
        return image.src ? image : null;
      },
      rows,
    ),
    loadRows(museumSourcesQuery(museum.slug), mapSourceRow, rows),
  ]);

  return {
    ...museum,
    exhibits,
    gallery,
    sources,
    imageUrl: museum.imageUrl ?? gallery[0]?.src ?? null,
  };
}
