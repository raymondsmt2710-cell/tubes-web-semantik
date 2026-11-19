"use client";

import { useState } from "react";
import { FALLBACK_IMAGE } from "@/lib/types";

interface MuseumImageProps {
  src: string | null;
  alt: string;
}

/**
 * Gambar museum dengan cadangan lokal. Bila URL kosong atau gagal dimuat,
 * pengganti SVG dipakai supaya halaman tidak pernah menampilkan ikon rusak.
 */
export default function MuseumImage({ src, alt }: MuseumImageProps) {
  const [failed, setFailed] = useState(false);
  const resolved = !src || failed ? FALLBACK_IMAGE : src;

  return (
    <figure className="border border-[--rule] bg-[--paper-2] rounded-sm overflow-hidden">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={resolved}
        alt={alt}
        onError={() => setFailed(true)}
        className="w-full aspect-[4/3] object-cover"
      />
      <figcaption className="px-3 py-2 text-xs text-[--ink-faint] border-t border-[--rule]">
        {failed || !src
          ? "Gambar belum tersedia untuk museum ini."
          : "Foto dari sumber data museum."}
      </figcaption>
    </figure>
  );
}
