"""Demo ujung-ke-ujung lapisan semantik Museum Sumatera.

Menjalankan lima demo yang mengikuti urutan materi:

    A. Ringkasan graf dan penalaran (P12)
    B. Hierarki kelas dan materialisasi ``CONSTRUCT`` (P11)
    C. Pencarian dengan ``SELECT`` (P9–P10)
    D. Benang merah dengan ``CONSTRUCT`` (P11)
    E. GraphRAG + NL2SPARQL: pertanyaan bahasa alami jadi jawaban ber-sumber (P13)

Jalankan dari folder ``pyapp/``::

    python scripts/demo.py
    python scripts/demo.py "Berapa jumlah pameran di Museum Negeri Aceh?"
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semweb.construct import materialisasi, verifikasi_hierarki  # noqa: E402
from semweb.graphrag import jangkar, pola_retrieval  # noqa: E402
from semweb.nl2sparql import aman, jawab  # noqa: E402
from semweb.relations import benang_merah  # noqa: E402
from semweb.search import cari_museum, daftar_provinsi  # noqa: E402
from semweb.store import MuseumStore  # noqa: E402

AKAR = Path(__file__).resolve().parents[2]
DATA = AKAR / "data" / "museum-sumatera.ttl"

PERTANYAAN_UJI = [
    "Museum apa saja yang ada di Aceh?",
    "Berapa jumlah museum?",
    "Berapa tahun Museum Negeri Aceh berdiri?",
    "Apa saja pameran di Museum Negeri Aceh?",
    "Museum apa yang ada di kota Banda Aceh?",
]


def judul(teks: str) -> None:
    print()
    print("=" * 72)
    print(teks)
    print("=" * 72)


def demo_a(store: MuseumStore) -> None:
    judul("A · Ringkasan graf dan penalaran (P12)")
    angka = store.ringkasan()
    print(f"  Triple ditulis (asserted) : {angka['asserted']}")
    print(f"  Closure RDFS              : {angka['closure_rdfs']}")
    print(f"  Closure OWL-RL            : {angka['closure']}")
    print(f"  Triple hasil inferensi    : {angka['inferred']}")
    print("  Reasoner tidak mengubah fakta yang ditulis; ia menambah fakta baru.")


def demo_b(store: MuseumStore) -> None:
    judul("B · Hierarki kelas dan materialisasi CONSTRUCT (P11)")
    print("  Subkelas sdp:Museum (operator +):")
    for baris in verifikasi_hierarki(store):
        print(f"    - {baris['lokal']:<14} {baris['individu']:>3} individu")

    turunan, angka = materialisasi(store)
    print()
    print(f"  Triple dicetak CONSTRUCT  : {angka['dicetak']}")
    print(f"  Sudah ada di graf         : {angka['sudah_ada']}  (cetakan kembar, graf = himpunan)")
    print(f"  Benar-benar baru          : {angka['baru']}")
    print(f"  Total triple graf turunan : {len(turunan)}")


def demo_c(store: MuseumStore) -> None:
    judul("C · Pencarian dengan SPARQL SELECT (P9–P10)")
    print("  Provinsi di graf:", ", ".join(daftar_provinsi(store)))
    for kueri in ("aceh", "perunggu", "kereta"):
        hasil = cari_museum(store, q=kueri, batas=5)
        nama = [h["nama"] for h in hasil]
        print(f"  q={kueri!r:<10} -> {len(hasil)} hasil: {', '.join(nama[:3])}")


def demo_d(store: MuseumStore) -> None:
    judul("D · Benang merah dengan CONSTRUCT (P11)")
    hasil = benang_merah(store, "museum-negeri-aceh", maks=4)
    for baris in hasil:
        print(f"    {baris['skor']:>2}  {baris['nama']:<38} {baris['alasan']}")


def demo_e(store: MuseumStore, pertanyaan: str) -> None:
    judul("E · GraphRAG + NL2SPARQL (P13)")

    print(f"  Pertanyaan: {pertanyaan}")

    temuan = jangkar(store, pertanyaan)
    if temuan:
        print("  Jangkar GraphRAG:")
        for j in temuan:
            print(f"    - {j.label}  ({j.jenis})  {j.iri}")
    else:
        print("  Jangkar GraphRAG: (tidak ada entitas yang dikenali)")

    _, jejak = pola_retrieval(store, pertanyaan, hop=1)
    if jejak:
        print()
        print("  Jejak retrieval:")
        for langkah in jejak:
            print(f"    {langkah.pola}: {len(langkah.triple)} triple")

    hasil = jawab(pertanyaan, store)
    print()
    print(f"  Query (lolos guard: {aman(hasil.query, store)[0]}):")
    for baris in hasil.query.strip().splitlines()[-8:]:
        print(f"    {baris}")
    print()
    print("  Jawaban:")
    for baris in hasil.jawaban.splitlines():
        print(f"    {baris}")


def main() -> int:
    if not DATA.exists():
        print(f"Berkas Turtle tidak ditemukan: {DATA}", file=sys.stderr)
        print("Jalankan dulu: python scripts/generate.py", file=sys.stderr)
        return 1

    store = MuseumStore.dari_turtle(DATA)

    demo_a(store)
    demo_b(store)
    demo_c(store)
    demo_d(store)

    if len(sys.argv) > 1:
        demo_e(store, " ".join(sys.argv[1:]))
    else:
        for pertanyaan in PERTANYAAN_UJI:
            demo_e(store, pertanyaan)

    print()
    print("Selesai.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
