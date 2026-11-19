"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

interface SearchBoxProps {
  defaultValue?: string;
  placeholder?: string;
  size?: "hero" | "inline";
}

export default function SearchBox({
  defaultValue = "",
  placeholder = "Cari museum, kota, atau tema…",
  size = "hero",
}: SearchBoxProps) {
  const router = useRouter();
  const [query, setQuery] = useState(defaultValue);

  function submit(event: React.FormEvent) {
    event.preventDefault();
    const params = new URLSearchParams();
    if (query.trim()) params.set("q", query.trim());
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
