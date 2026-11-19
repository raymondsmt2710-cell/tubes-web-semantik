"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export type CatalogSort = "name" | "year";
export type CatalogOrder = "asc" | "desc";

interface CatalogPrefsState {
  sort: CatalogSort;
  order: CatalogOrder;
  setSort: (sort: CatalogSort) => void;
  setOrder: (order: CatalogOrder) => void;
  reset: () => void;
}

/**
 * Preferensi tampilan katalog yang bertahan antar kunjungan. Yang disimpan
 * hanya cara mengurutkan; filter penyaring selalu ikut URL agar tautan tetap
 * bisa dibagikan apa adanya.
 */
export const useCatalogPrefs = create<CatalogPrefsState>()(
  persist(
    (set) => ({
      sort: "name",
      order: "asc",
      setSort: (sort) => set({ sort }),
      setOrder: (order) => set({ order }),
      reset: () => set({ sort: "name", order: "asc" }),
    }),
    { name: "museum-catalog-prefs" },
  ),
);
