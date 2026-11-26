import { NextResponse } from "next/server";
import { FusekiError, runSelect } from "@/lib/sparql";
import { askGraph } from "@/lib/nl2sparql";

export const dynamic = "force-dynamic";

/**
 * Endpoint tanya-jawab bahasa alami (GraphRAG + NL2SPARQL).
 *
 * Alurnya mengikuti materi P13 dan seluruhnya dijalankan di server:
 * 1. Pertanyaan diterjemahkan menjadi query SPARQL.
 * 2. Query diperiksa guard (hanya SELECT, LIMIT, IRI dikenal).
 * 3. Query yang lolos dijalankan ke Fuseki.
 * 4. Jawaban disusun dari data, dan IRI sumber ditempel oleh kode.
 *
 * Guard memeriksa **bentuk** query, bukan hak akses pengguna (P13 bagian 28).
 */
export async function GET(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const pertanyaan = (url.searchParams.get("q") ?? "").trim();

  if (!pertanyaan) {
    return NextResponse.json(
      { error: "Sertakan parameter q berisi pertanyaan." },
      { status: 400 },
    );
  }

  if (pertanyaan.length > 300) {
    return NextResponse.json(
      { error: "Pertanyaan terlalu panjang (maksimal 300 karakter)." },
      { status: 400 },
    );
  }

  try {
    const hasil = await askGraph(pertanyaan, runSelect);
    return NextResponse.json(hasil);
  } catch (error) {
    if (error instanceof FusekiError) {
      return NextResponse.json(
        {
          error: "Tidak dapat terhubung ke basis data museum.",
          detail: error.message,
        },
        { status: 502 },
      );
    }

    return NextResponse.json(
      {
        error: "Terjadi kesalahan saat menjawab pertanyaan.",
        detail: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
}
