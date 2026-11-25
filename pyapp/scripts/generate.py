"""Hasilkan `data/museum-sumatera.ttl` dari `data/museums.json`.

Jalankan dari folder `pyapp/`:

    python scripts/generate.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from semweb.generator import load_records, ringkasan, tulis_ttl  # noqa: E402

AKAR = Path(__file__).resolve().parents[2]
SUMBER = AKAR / "data" / "museums.json"
TUJUAN = AKAR / "data" / "museum-sumatera.ttl"


def main() -> int:
    if not SUMBER.exists():
        print(f"Data sumber tidak ditemukan: {SUMBER}", file=sys.stderr)
        return 1

    records = load_records(SUMBER)
    path = tulis_ttl(records, TUJUAN)
    angka = ringkasan(records)

    print(f"Turtle ditulis ke {path}")
    print(f"  ukuran     : {path.stat().st_size / 1024:.1f} KB")
    for kunci in ("museum", "provinsi", "tema", "bab", "pameran", "foto"):
        print(f"  {kunci:<11}: {angka[kunci]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
