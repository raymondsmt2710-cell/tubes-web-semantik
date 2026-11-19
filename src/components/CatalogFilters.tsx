"use client";

import { hasActiveFilters } from "@/lib/catalogParams";
import type { CatalogParams } from "@/lib/queries";
import {
  ERAS,
  ERAS_LABELS,
  PROVINCES,
  THEMES,
  THEME_LABELS,
  type Era,
  type Theme,
} from "@/lib/types";

interface CatalogFiltersProps {
  value: CatalogParams;
  onChange: (next: CatalogParams) => void;
  disabled?: boolean;
}

export default function CatalogFilters({
  value,
  onChange,
  disabled = false,
}: CatalogFiltersProps) {
  function set<K extends keyof CatalogParams>(key: K, next: CatalogParams[K]) {
    onChange({ ...value, [key]: next });
  }

  function setMinYear(raw: string) {
    const parsed = raw.trim() ? Number(raw) : Number.NaN;
    set("minYear", Number.isFinite(parsed) ? Math.trunc(parsed) : undefined);
  }

  return (
    <fieldset
      disabled={disabled}
      className="mt-6 border border-[--rule] bg-[--paper-2]/60 rounded-sm px-4 py-4 sm:px-5"
    >
      <legend className="label px-1">Penyaringan</legend>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <label className="block">
          <span className="label">Provinsi</span>
          <select
            className="mt-1"
            value={value.province ?? ""}
            onChange={(event) => set("province", event.target.value || undefined)}
          >
            <option value="">Semua provinsi</option>
            {PROVINCES.map((province) => (
              <option key={province} value={province}>
                {province}
              </option>
            ))}
          </select>
        </label>

        <label className="block">
          <span className="label">Tema</span>
          <select
            className="mt-1"
            value={value.theme ?? ""}
            onChange={(event) => set("theme", event.target.value || undefined)}
          >
            <option value="">Semua tema</option>
            {THEMES.map((theme) => (
              <option key={theme} value={theme}>
                {THEME_LABELS[theme as Theme]}
              </option>
            ))}
          </select>
        </label>

        <label className="block">
          <span className="label">Era</span>
          <select
            className="mt-1"
            value={value.era ?? ""}
            onChange={(event) => set("era", event.target.value || undefined)}
          >
            <option value="">Semua era</option>
            {ERAS.map((era) => (
              <option key={era} value={era}>
                {ERAS_LABELS[era as Era]}
              </option>
            ))}
          </select>
        </label>

        <label className="block">
          <span className="label">Berdiri sejak tahun</span>
          <input
            className="mt-1"
            type="number"
            inputMode="numeric"
            min={1000}
            max={2100}
            placeholder="mis. 1900"
            value={value.minYear ?? ""}
            onChange={(event) => setMinYear(event.target.value)}
          />
        </label>

        <label className="block">
          <span className="label">Urutkan</span>
          <select
            className="mt-1"
            value={value.sort ?? "name"}
            onChange={(event) =>
              set("sort", event.target.value === "year" ? "year" : "name")
            }
          >
            <option value="name">Nama museum</option>
            <option value="year">Tahun berdiri</option>
          </select>
        </label>

        <label className="block">
          <span className="label">Arah urutan</span>
          <select
            className="mt-1"
            value={value.order ?? "asc"}
            onChange={(event) =>
              set("order", event.target.value === "desc" ? "desc" : "asc")
            }
          >
            <option value="asc">Menaik</option>
            <option value="desc">Menurun</option>
          </select>
        </label>
      </div>

      {hasActiveFilters(value) && (
        <button
          type="button"
          className="btn btn-ghost mt-4 text-xs"
          onClick={() => onChange({ sort: value.sort, order: value.order })}
        >
          Bersihkan penyaringan
        </button>
      )}
    </fieldset>
  );
}
