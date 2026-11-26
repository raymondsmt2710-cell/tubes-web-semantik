"use client";

import { useState } from "react";

interface AskJawaban {
  pertanyaan: string;
  query: string;
  lolos: boolean;
  pesan: string;
  jawaban: string;
  sumber: string[];
  baris: string[][];
}

const CONTOH = [
  "Museum apa saja yang ada di Aceh?",
  "Berapa jumlah museum?",
  "Berapa tahun Museum Negeri Aceh berdiri?",
  "Apa saja pameran di Museum Negeri Aceh?",
  "Museum apa yang ada di kota Banda Aceh?",
];

/**
 * Kotak tanya-jawab bahasa alami.
 *
 * Yang ditampilkan bukan hanya jawaban: query SPARQL, hasil guard, dan IRI
 * sumber ikut ditampilkan supaya pengguna dapat memeriksa dari mana jawaban
 * berasal. Ini inti P13 — "graf tahu faktanya, model tahu bahasanya".
 */
export function AskPanel() {
  const [pertanyaan, setPertanyaan] = useState("");
  const [hasil, setHasil] = useState<AskJawaban | null>(null);
  const [galat, setGalat] = useState<string | null>(null);
  const [memuat, setMemuat] = useState(false);
  const [tampilQuery, setTampilQuery] = useState(false);

  async function kirim(teks: string) {
    const q = teks.trim();
    if (!q || memuat) return;

    setMemuat(true);
    setGalat(null);
    setHasil(null);

    try {
      const res = await fetch(`/api/tanya?q=${encodeURIComponent(q)}`, {
        cache: "no-store",
      });
      const body = await res.json();

      if (!res.ok) {
        setGalat(body.error ?? "Pertanyaan gagal dijawab.");
      } else {
        setHasil(body as AskJawaban);
      }
    } catch {
      setGalat("Tidak dapat menghubungi server.");
    } finally {
      setMemuat(false);
    }
  }

  return (
    <div>
      <form
        className="mt-6"
        onSubmit={(event) => {
          event.preventDefault();
          void kirim(pertanyaan);
        }}
      >
        <label htmlFor="pertanyaan" className="label">
          Pertanyaan
        </label>
        <div className="mt-2 flex flex-col gap-2 sm:flex-row">
          <input
            id="pertanyaan"
            type="text"
            value={pertanyaan}
            onChange={(event) => setPertanyaan(event.target.value)}
            placeholder="Misalnya: museum apa saja yang ada di Aceh?"
            maxLength={300}
            className="flex-1 rounded-sm border border-[--ink-faint] bg-[--paper] px-3 py-2 text-sm"
          />
          <button
            type="submit"
            disabled={memuat || !pertanyaan.trim()}
            className="rounded-sm border border-[--ink] px-4 py-2 text-sm disabled:opacity-40"
          >
            {memuat ? "Mencari…" : "Tanya"}
          </button>
        </div>
      </form>

      <div className="mt-4">
        <p className="label">Contoh pertanyaan</p>
        <ul className="mt-2 flex flex-wrap gap-2">
          {CONTOH.map((contoh) => (
            <li key={contoh}>
              <button
                type="button"
                className="rounded-full border border-[--ink-faint] px-3 py-1 text-xs text-[--ink-soft] hover:border-[--ink]"
                onClick={() => {
                  setPertanyaan(contoh);
                  void kirim(contoh);
                }}
              >
                {contoh}
              </button>
            </li>
          ))}
        </ul>
      </div>

      {galat && (
        <p className="mt-6 rounded-sm border border-[--ink-faint] bg-[--paper-deep] p-3 text-sm">
          {galat}
        </p>
      )}

      {hasil && (
        <div className="mt-8 space-y-5">
          <section>
            <p className="label">Jawaban</p>
            <div className="mt-2 whitespace-pre-line text-sm measure">{hasil.jawaban}</div>
          </section>

          {hasil.sumber.length > 0 && (
            <section>
              <p className="label">Sumber (IRI di graf)</p>
              <ul className="mt-2 space-y-1">
                {hasil.sumber.map((iri) => (
                  <li key={iri} className="font-mono text-xs text-[--ink-soft] break-all">
                    {iri}
                  </li>
                ))}
              </ul>
            </section>
          )}

          <section>
            <div className="flex items-center justify-between">
              <p className="label">
                Query SPARQL · guard: {hasil.lolos ? "lolos" : `ditolak (${hasil.pesan})`}
              </p>
              <button
                type="button"
                className="text-xs underline"
                onClick={() => setTampilQuery((v) => !v)}
              >
                {tampilQuery ? "Sembunyikan" : "Tampilkan"}
              </button>
            </div>
            {tampilQuery && (
              <pre className="mt-2 overflow-x-auto rounded-sm border border-[--ink-faint] bg-[--paper-deep] p-3 text-xs">
                {hasil.query}
              </pre>
            )}
          </section>

          {hasil.baris.length > 0 && (
            <section>
              <p className="label">Baris hasil ({hasil.baris.length})</p>
              <div className="mt-2 overflow-x-auto">
                <table className="w-full text-xs">
                  <tbody>
                    {hasil.baris.slice(0, 10).map((baris, index) => (
                      <tr key={index} className="border-b border-[--ink-faint]">
                        {baris.map((sel, selIndex) => (
                          <td key={selIndex} className="py-1 pr-3 align-top">
                            {sel}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}
        </div>
      )}
    </div>
  );
}
