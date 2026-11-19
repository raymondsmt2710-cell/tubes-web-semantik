import type { CatalogParams } from "./queries";

function clean(value: string | null): string | undefined {
  const trimmed = value?.trim();
  return trimmed ? trimmed : undefined;
}

/**
 * Membaca keadaan katalog dari URL. URL adalah sumber kebenaran supaya hasil
 * pencarian bisa dibagikan dan dimuat ulang tanpa kehilangan filter.
 */
export function parseCatalogParams(search: URLSearchParams): CatalogParams {
  const minYearRaw = search.get("minYear");
  const parsedYear = minYearRaw?.trim() ? Number(minYearRaw) : Number.NaN;

  return {
    q: clean(search.get("q")),
    province: clean(search.get("province")),
    theme: clean(search.get("theme")),
    era: clean(search.get("era")),
    minYear: Number.isFinite(parsedYear) ? Math.trunc(parsedYear) : undefined,
    sort: search.get("sort") === "year" ? "year" : "name",
    order: search.get("order") === "desc" ? "desc" : "asc",
  };
}

/** Menulis hanya nilai yang terisi, dengan urutan kunci yang stabil. */
export function buildCatalogQuery(params: CatalogParams): string {
  const search = new URLSearchParams();

  if (params.q?.trim()) search.set("q", params.q.trim());
  if (params.province?.trim()) search.set("province", params.province.trim());
  if (params.theme?.trim()) search.set("theme", params.theme.trim());
  if (params.era?.trim()) search.set("era", params.era.trim());
  if (params.minYear !== undefined && Number.isFinite(params.minYear)) {
    search.set("minYear", String(Math.trunc(params.minYear)));
  }
  if (params.sort) search.set("sort", params.sort);
  if (params.order) search.set("order", params.order);

  return search.toString();
}

/**
 * Pengurutan bukan penyaringan: memilih urutan tidak mempersempit hasil, jadi
 * empty state "tidak ada yang cocok" hanya muncul bila ada filter sungguhan.
 */
export function hasActiveFilters(params: CatalogParams): boolean {
  return Boolean(
    params.q?.trim() ||
      params.province?.trim() ||
      params.theme?.trim() ||
      params.era?.trim() ||
      (params.minYear !== undefined && Number.isFinite(params.minYear)),
  );
}
