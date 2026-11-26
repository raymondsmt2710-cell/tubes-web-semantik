"""Bandingkan penerjemah aturan dengan penerjemah model pada pertanyaan yang sama.

Dipakai untuk memenuhi kriteria C1: tabel perbandingan 10 pertanyaan, berisi
lolos-guard, benar-tidaknya jawaban, dan waktu respons.

Dua mode:

- Tanpa ``LLM_API_KEY``, skrip hanya menjalankan jalur aturan dan memberi tahu
  bahwa pembandingan tidak bisa dilakukan. Keluar dengan kode 0 — tidak adanya
  kunci bukan kegagalan.
- Dengan kunci, kedua jalur dijalankan dan hasilnya dicetak sebagai tabel.

Jawaban dianggap "benar" bila cocok dengan penanda yang ditulis di daftar
pertanyaan. Penanda itu bukan jawaban lengkap, hanya bukti bahwa query
mengarah ke hal yang ditanyakan.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR / "pyapp"))

from semweb.llm import adapter_dari_env
from semweb.nl2sparql import jawab
from semweb.store import MuseumStore

DATA_TTL = AKAR / "data" / "museum-sumatera.ttl"

PERTANYAAN: list[tuple[str, str]] = [
    ("museum apa saja di Aceh?", "Museum"),
    ("ada berapa museum?", "28"),
    ("pameran apa saja di Museum Negeri Aceh?", "Lonceng"),
    ("kapan Museum Negeri Aceh berdiri?", "1915"),
    ("museum apa saja yang bertema etnografi?", "Museum"),
    ("berapa pameran di Museum Tsunami Aceh?", "4"),
    ("museum di kota Banda Aceh?", "Museum"),
    ("provinsi apa saja yang punya museum?", "Aceh"),
    ("museum yang berdiri sebelum 1950?", "Museum"),
    ("berapa harga tiket pesawat ke Aceh?", ""),
]


def _jalankan(store: MuseumStore, pertanyaan: str, penanda: str, penerjemah) -> dict:
    mulai = time.perf_counter()
    hasil = jawab(pertanyaan, store, penerjemah=penerjemah)
    durasi = (time.perf_counter() - mulai) * 1000
    benar = bool(penanda) and penanda.lower() in hasil.jawaban.lower()
    return {
        "lolos": hasil.lolos,
        "benar": benar,
        "ms": durasi,
        "jawaban": hasil.jawaban,
    }


def _tabel(baris: list[dict]) -> str:
    kepala = f"{'#':>2}  {'pertanyaan':<46} {'guard':<7} {'benar':<6} {'ms':>7}"
    garis = "-" * len(kepala)
    isi = [kepala, garis]
    for i, b in enumerate(baris, 1):
        guard = "lolos" if b["aturan"]["lolos"] else "tolak"
        benar = "ya" if b["aturan"]["benar"] else "tidak"
        isi.append(f"{i:>2}  {b['tanya'][:46]:<46} {guard:<7} {benar:<6} {b['aturan']['ms']:>7.1f}")
    return "\n".join(isi)


def main() -> int:
    store = MuseumStore.dari_turtle(DATA_TTL)
    adapter = adapter_dari_env()

    baris: list[dict] = []
    for pertanyaan, penanda in PERTANYAAN:
        baris.append(
            {
                "tanya": pertanyaan,
                "penanda": penanda,
                "aturan": _jalankan(store, pertanyaan, penanda, None),
                "model": _jalankan(store, pertanyaan, penanda, adapter) if adapter else None,
            }
        )

    print("== Penerjemah aturan ==")
    print(_tabel(baris))

    if adapter is None:
        print(
            "\nLLM_API_KEY belum diisi, jadi jalur model tidak dijalankan.\n"
            "Isi LLM_API_KEY dan LLM_PROVIDER di .env untuk membandingkan."
        )
        return 0

    print("\n== Penerjemah model ==")
    print(f"{'#':>2}  {'pertanyaan':<46} {'guard':<7} {'benar':<6} {'ms':>7}")
    print("-" * 70)
    for i, b in enumerate(baris, 1):
        m = b["model"]
        guard = "lolos" if m["lolos"] else "tolak"
        benar = "ya" if m["benar"] else "tidak"
        print(f"{i:>2}  {b['tanya'][:46]:<46} {guard:<7} {benar:<6} {m['ms']:>7.1f}")

    lolos_a = sum(1 for b in baris if b["aturan"]["lolos"])
    lolos_m = sum(1 for b in baris if b["model"]["lolos"])
    benar_a = sum(1 for b in baris if b["aturan"]["benar"])
    benar_m = sum(1 for b in baris if b["model"]["benar"])
    rata_a = sum(b["aturan"]["ms"] for b in baris) / len(baris)
    rata_m = sum(b["model"]["ms"] for b in baris) / len(baris)

    print(
        f"\nRingkasan: lolos guard aturan {lolos_a}/{len(baris)}, model {lolos_m}/{len(baris)}. "
        f"Jawaban benar aturan {benar_a}/{len(baris)}, model {benar_m}/{len(baris)}. "
        f"Rata-rata waktu aturan {rata_a:.1f} ms, model {rata_m:.1f} ms."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
