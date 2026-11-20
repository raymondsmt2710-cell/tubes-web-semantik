import { NextResponse } from "next/server";
import { runSelect, FusekiError } from "@/lib/sparql";
import { mapMuseumRow, searchCatalogQuery, type CatalogParams } from "@/lib/queries";
import { rankMuseums } from "@/lib/ranking";
import type { CatalogResponse, MuseumDTO } from "@/lib/types";

export const dynamic = "force-dynamic";

function readParams(url: URL): CatalogParams {
  const search = url.searchParams;
  const sortParam = search.get("sort");
  const orderParam = search.get("order");
  const minYearRaw = search.get("minYear");

  return {
    q: search.get("q")?.trim() || undefined,
    province: search.get("province")?.trim() || undefined,
    theme: search.get("theme")?.trim() || undefined,
    era: search.get("era")?.trim() || undefined,
    minYear: minYearRaw ? Number(minYearRaw) : undefined,
    sort: sortParam === "year" || sortParam === "name" ? sortParam : "name",
    order: orderParam === "desc" ? "desc" : "asc",
  };
}

export async function GET(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const params = readParams(url);

  try {
    const rows = await runSelect(searchCatalogQuery(params));
    const museums: MuseumDTO[] = rows.map(mapMuseumRow);

    if (!params.q) {
      const body: CatalogResponse = { museums, total: museums.length };
      return NextResponse.json(body);
    }

    const { primary, secondary, scores } = rankMuseums(
      museums,
      params.q,
      (museum) =>
        [
          museum.name,
          museum.city,
          museum.province,
          museum.era,
          museum.description,
          museum.themes.join(" "),
        ]
          .filter(Boolean)
          .join(" "),
    );
    const ordered = [...primary, ...secondary];
    const primarySlugs = new Set(primary.map((museum) => museum.slug));

    const body: CatalogResponse = {
      museums: ordered,
      total: ordered.length,
      ranking: ordered.map((museum) => ({
        slug: museum.slug,
        score: Number((scores.get(museum.name) ?? 0).toFixed(3)),
        group: primarySlugs.has(museum.slug) ? "primary" : "secondary",
      })),
    };

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
        error: "Terjadi kesalahan saat mencari museum.",
        detail: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
}
