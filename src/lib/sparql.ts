import { FUSEKI_DEFAULT_ENDPOINT } from "./types";

export interface SparqlValue {
  type: string;
  value: string;
  "xml:lang"?: string;
  datatype?: string;
}

export type SparqlBinding = Record<string, SparqlValue | undefined>;

export interface SparqlResults {
  results: {
    bindings: SparqlBinding[];
  };
}

export class FusekiError extends Error {
  status?: number;
  detail?: string;

  constructor(message: string, status?: number, detail?: string) {
    super(message);
    this.name = "FusekiError";
    this.status = status;
    this.detail = detail;
  }
}

export function fusekiEndpoint(): string {
  return process.env.FUSEKI_ENDPOINT?.trim() || FUSEKI_DEFAULT_ENDPOINT;
}

/**
 * Menjalankan SELECT terhadap Fuseki. Semua query aplikasi lewat sini supaya
 * penanganan error dan format respons hanya ada di satu tempat.
 */
export async function runSelect(query: string): Promise<SparqlBinding[]> {
  const endpoint = fusekiEndpoint();

  let response: Response;
  try {
    response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Accept: "application/sparql-results+json",
      },
      body: `query=${encodeURIComponent(query)}`,
      cache: "no-store",
    });
  } catch (error) {
    throw new FusekiError(
      "Tidak dapat terhubung ke basis data museum.",
      undefined,
      error instanceof Error ? error.message : String(error),
    );
  }

  if (!response.ok) {
    const detail = await response.text().catch(() => "");
    throw new FusekiError(
      "Basis data museum menolak permintaan.",
      response.status,
      detail.slice(0, 500),
    );
  }

  let data: SparqlResults;
  try {
    data = (await response.json()) as SparqlResults;
  } catch {
    throw new FusekiError("Respons basis data museum tidak dapat dibaca.", response.status);
  }

  if (!data?.results?.bindings) {
    throw new FusekiError("Respons basis data museum tidak berisi hasil.");
  }

  return data.results.bindings;
}

/** Escape literal SPARQL (string di dalam tanda kutip ganda). */
export function sparqlString(value: string): string {
  return value
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/'/g, "\\'")
    .replace(/\r/g, "\\r")
    .replace(/\n/g, "\\n")
    .replace(/\t/g, "\\t");
}
