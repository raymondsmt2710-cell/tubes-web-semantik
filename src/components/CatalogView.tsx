"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import CatalogFilters from "@/components/CatalogFilters";
import EmptyState from "@/components/EmptyState";
import MuseumEntry from "@/components/MuseumEntry";
import SearchBox from "@/components/SearchBox";
import {
  buildCatalogQuery,
  hasActiveFilters,
  parseCatalogParams,
} from "@/lib/catalogParams";
import type { CatalogParams } from "@/lib/queries";
import type { CatalogResponse, MuseumDTO } from "@/lib/types";
import { useCatalogPrefs } from "@/store/catalogPrefs";

type LoadState =
  | { status: "loading" }
  | { status: "ready"; data: CatalogResponse }
  | { status: "error"; message: string };

interface Grouped {
  primary: MuseumDTO[];
  secondary: MuseumDTO[];
}

/**
 * Mengelompokkan hasil sesuai penanda dari API. Ini hanya penataan tampilan:
 * pemilihan museum dan urutannya sudah ditentukan di sisi SPARQL/route.
 */
function groupByRanking(data: CatalogResponse): Grouped {
  const primary: MuseumDTO[] = [];
  const secondary: MuseumDTO[] = [];

  if (!data.ranking) {
    return { primary: data.museums, secondary: [] };
  }

  const bySlug = new Map<string, MuseumDTO>();
  for (const museum of data.museums) bySlug.set(museum.slug, museum);

  for (const entry of data.ranking) {
    const museum = bySlug.get(entry.slug);
    if (!museum) continue;
    if (entry.group === "primary") primary.push(museum);
    else secondary.push(museum);
  }

  return { primary, secondary };
}

export default function CatalogView() {
  const searchParams = useSearchParams();
  const [params, setParams] = useState<CatalogParams>(() =>
    parseCatalogParams(new URLSearchParams(searchParams.toString())),
  );
  const [state, setState] = useState<LoadState>({ status: "loading" });
  const [retryToken, setRetryToken] = useState(0);

  const paramsQuery = buildCatalogQuery(params);
  const filtered = hasActiveFilters(params);

  const setSavedSort = useCatalogPrefs((store) => store.setSort);
  const setSavedOrder = useCatalogPrefs((store) => store.setOrder);

  function update(next: CatalogParams) {
    setParams(next);
    const query = buildCatalogQuery(next);
    window.history.replaceState(
      null,
      "",
      query ? `/katalog?${query}` : "/katalog",
    );
  }

  // Terapkan preferensi urutan terakhir hanya bila URL tidak menyebutkannya.
  useEffect(() => {
    const search = new URLSearchParams(window.location.search);
    if (search.has("sort") || search.has("order")) return;

    const prefs = useCatalogPrefs.getState();
    const current = parseCatalogParams(search);
    if (current.sort === prefs.sort && current.order === prefs.order) return;

    const next = { ...current, sort: prefs.sort, order: prefs.order };
    setParams(next);
    window.history.replaceState(null, "", `/katalog?${buildCatalogQuery(next)}`);
  }, []);

  // Dukung tombol kembali/maju browser tanpa menambah entri riwayat sendiri.
  useEffect(() => {
    function syncFromUrl() {
      setParams(
        parseCatalogParams(new URLSearchParams(window.location.search)),
      );
    }
    window.addEventListener("popstate", syncFromUrl);
    return () => window.removeEventListener("popstate", syncFromUrl);
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading" });

    fetch(`/api/search${paramsQuery ? `?${paramsQuery}` : ""}`, {
      signal: controller.signal,
      cache: "no-store",
    })
      .then(async (response) => {
        const body = (await response.json().catch(() => null)) as
          | CatalogResponse
          | { error?: string }
          | null;

        if (!response.ok) {
          const message =
            body && "error" in body && body.error
              ? body.error
              : "Katalog museum tidak dapat dimuat.";
          throw new Error(message);
        }

        setState({ status: "ready", data: body as CatalogResponse });
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === "AbortError") return;
        const raw = error instanceof Error ? error.message : "";
        setState({
          status: "error",
          message:
            raw && raw !== "Failed to fetch"
              ? raw
              : "Tidak dapat menghubungi server katalog.",
        });
      });

    return () => controller.abort();
  }, [paramsQuery, retryToken]);

  function handleChange(next: CatalogParams) {
    if (next.sort && next.sort !== params.sort) setSavedSort(next.sort);
    if (next.order && next.order !== params.order) setSavedOrder(next.order);
    update(next);
  }

  function resetFilters() {
    update({ sort: params.sort, order: params.order });
  }

  const grouped =
    state.status === "ready" ? groupByRanking(state.data) : null;
  const hasRanking = Boolean(
    state.status === "ready" && state.data.ranking,
  );

  return (
    <>
      <div className="mt-8 max-w-xl">
        <SearchBox
          size="inline"
          defaultValue={params.q ?? ""}
          onSearch={(query) => update({ ...params, q: query || undefined })}
          placeholder="Cari nama, kota, atau tema…"
        />
      </div>

      <CatalogFilters value={params} onChange={handleChange} />

      <section className="mt-8" aria-live="polite" aria-busy={state.status === "loading"}>
        {state.status === "loading" && (
          <p className="text-sm text-[--ink-soft]">Memuat katalog…</p>
        )}

        {state.status === "error" && (
          <div
            role="alert"
            className="border border-[--rule] bg-[--paper-2] rounded-sm px-5 py-6"
          >
            <p className="label">Gagal memuat</p>
            <h2 className="mt-2 text-lg">Basis data museum tidak dapat dihubungi</h2>
            <p className="mt-2 text-sm text-[--ink-soft] measure">
              {state.message} Pastikan Apache Jena Fuseki berjalan dan berkas RDF
              sudah diunggah.
            </p>
            <button
              type="button"
              className="btn btn-ghost mt-4"
              onClick={() => setRetryToken((token) => token + 1)}
            >
              Coba lagi
            </button>
          </div>
        )}

        {state.status === "ready" && state.data.total === 0 && (
          <EmptyState hasFilters={filtered} onReset={resetFilters} />
        )}

        {state.status === "ready" && state.data.total > 0 && grouped && (
          <>
            <div className="flex flex-wrap items-baseline justify-between gap-2 border-b border-[--rule] pb-2">
              <p className="text-sm">
                <span className="font-serif text-lg">{state.data.total}</span> museum
                {params.q ? ` untuk “${params.q}”` : ""}
              </p>
              {filtered && (
                <p className="label">Penyaringan aktif</p>
              )}
            </div>

            {hasRanking && grouped.primary.length > 0 && (
              <div className="mt-6">
                <h2 className="label mb-1">Hasil utama</h2>
                {grouped.primary.map((museum, position) => (
                  <MuseumEntry
                    key={museum.slug}
                    museum={museum}
                    index={position + 1}
                  />
                ))}
              </div>
            )}

            {hasRanking && grouped.secondary.length > 0 && (
              <div className="mt-8">
                <h2 className="label mb-1">
                  {grouped.primary.length === 0
                    ? "Tidak ada kecocokan kuat — hasil lain"
                    : "Hasil lainnya"}
                </h2>
                {grouped.secondary.map((museum, position) => (
                  <MuseumEntry
                    key={museum.slug}
                    museum={museum}
                    index={grouped.primary.length + position + 1}
                  />
                ))}
              </div>
            )}

            {!hasRanking && (
              <div className="mt-2">
                {grouped.primary.map((museum, position) => (
                  <MuseumEntry
                    key={museum.slug}
                    museum={museum}
                    index={position + 1}
                  />
                ))}
              </div>
            )}
          </>
        )}
      </section>
    </>
  );
}
