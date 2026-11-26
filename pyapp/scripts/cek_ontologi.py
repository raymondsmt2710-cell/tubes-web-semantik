"""Periksa kepatuhan ontologi museum terhadap data yang dipakai aplikasi.

Menggantikan pemeriksaan manual di Protégé (HermiT) dengan skrip yang bisa
diulang dan dipakai di CI. Jalankan dari folder ``pyapp/``:

    python scripts/cek_ontologi.py
    python scripts/cek_ontologi.py --ontologi ../ontology/museum-sumatera.ttl

Keluar dengan kode 0 bila ontologi patuh, 1 bila ada temuan. Kode 1 dipakai
agar skrip bisa dipasang sebagai gerbang sebelum merge.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rdflib import Graph  # noqa: E402

from semweb.ontologi import periksa_ontologi  # noqa: E402

AKAR = Path(__file__).resolve().parents[2]
ONTO = AKAR / "ontology" / "museum-sumatera.ttl"
DATA = AKAR / "data" / "museum-sumatera.ttl"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Periksa kepatuhan ontologi museum terhadap data."
    )
    parser.add_argument("--ontologi", default=str(ONTO), help="Berkas ontologi Turtle")
    parser.add_argument("--data", default=str(DATA), help="Berkas data Turtle")
    args = parser.parse_args()

    onto_path = Path(args.ontologi)
    data_path = Path(args.data)

    for berkas in (onto_path, data_path):
        if not berkas.exists():
            print(f"Berkas tidak ditemukan: {berkas}", file=sys.stderr)
            return 1

    onto = Graph().parse(onto_path, format="turtle")
    data = Graph().parse(data_path, format="turtle")
    temuan = periksa_ontologi(onto, data)

    print(f"Ontologi : {onto_path.name}")
    print(f"Data     : {data_path.name}")
    print(f"Aturan   : domain-range, makna-ganda, kelas-tak-deklarasi, "
          f"disjoint, subkelas-kosong")
    print()

    if not temuan:
        print("Ontologi lulus: tidak ada temuan.")
        return 0

    print(f"Ditemukan {len(temuan)} temuan:")
    for t in temuan:
        print(f"  {t}")
    print()
    print("Perbaiki ontologi atau data, lalu jalankan ulang skrip ini.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
