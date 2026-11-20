"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

interface SearchBoxProps {
  defaultValue?: string;
  placeholder?: string;
  size?: "hero" | "inline";
  /** Bila diisi, pencarian ditangani pemanggil (mis. halaman katalog). */
  onSearch?: (query: string) => void;
}

export default function SearchBox({
  defaultValue = "",
  placeholder = "Cari nama museum, kota, atau tema, mis. Medan…",
  size = "hero",
  onSearch,
}: SearchBoxProps) {
  const router = useRouter();
  const [query, setQuery] = useState(defaultValue);

  useEffect(() => {
    setQuery(defaultValue);
  }, [defaultValue]);

  function submit(event: React.FormEvent) {
    event.preventDefault();
    const trimmed = query.trim();

    if (onSearch) {
      onSearch(trimmed);
      return;
    }

    const params = new URLSearchParams();
    if (trimmed) params.set("q", trimmed);
    router.push(`/katalog${params.toString() ? `?${params.toString()}` : ""}`);
  }

  return (
    <form onSubmit={submit} className="flex gap-2 w-full" role="search">
      <label className="sr-only" htmlFor="museum-search">
        Kata kunci pencarian museum
      </label>
      <input
        id="museum-search"
        type="search"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder={placeholder}
        className={size === "hero" ? "text-base" : "text-sm"}
        autoComplete="off"
      />
      <button type="submit" className="btn whitespace-nowrap">
        Cari
      </button>
    </form>
  );
}
