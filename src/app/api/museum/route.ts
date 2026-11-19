import { NextResponse } from "next/server";
import { runSelect, FusekiError } from "@/lib/sparql";
import { mapMuseumRow, museumBySlugQuery, relatedCandidatesQuery } from "@/lib/queries";
import { pickRelated } from "@/lib/related";
import type { MuseumResponse } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const slug = url.searchParams.get("slug")?.trim();

  if (!slug) {
    return NextResponse.json(
      { error: "Parameter slug wajib diisi." },
      { status: 400 },
    );
  }

  try {
    const rows = await runSelect(museumBySlugQuery(slug));

    if (rows.length === 0) {
      return NextResponse.json(
        { error: "Museum tidak ditemukan." },
        { status: 404 },
      );
    }

    const museum = mapMuseumRow(rows[0]);

    let related: MuseumResponse["related"] = [];
    try {
      const candidateRows = await runSelect(relatedCandidatesQuery(museum.slug));
      related = pickRelated(museum, candidateRows.map(mapMuseumRow));
    } catch {
      // Benang merah bersifat pelengkap: kegagalan query kedua tidak boleh
      // membuat seluruh halaman museum gagal.
      related = [];
    }

    const body: MuseumResponse = { museum, related };
    return NextResponse.json(body);
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
        error: "Terjadi kesalahan saat memuat museum.",
        detail: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
}
