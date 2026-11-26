"""Unggah graf museum ke Apache Jena Fuseki.

Memakai Graph Store Protocol: ``PUT {FUSEKI_UPDATE}?default`` mengganti seluruh
isi graph default dengan berkas Turtle, sehingga tidak ada sisa entri lama.

Jalankan dari folder ``pyapp/``::

    python scripts/upload_fuseki.py
    python scripts/upload_fuseki.py --endpoint http://localhost:3030/museum/data
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR / "pyapp"))

from semweb.env import baca_env

DATA = AKAR / "data" / "museum-sumatera.ttl"


def unggah(endpoint: str, isi: bytes, tipe: str = "text/turtle") -> None:
    """Kirim graf ke graph default lewat HTTP PUT."""
    permintaan = urllib.request.Request(
        url=endpoint + "?default",
        data=isi,
        method="PUT",
        headers={"Content-Type": tipe},
    )
    with urllib.request.urlopen(permintaan, timeout=120) as respons:
        if respons.status not in (200, 201, 204):
            raise RuntimeError(f"Fuseki membalas status {respons.status}")


def main() -> int:
    env = baca_env()
    bawaan = (
        os.environ.get("FUSEKI_UPDATE")
        or env.get("FUSEKI_UPDATE")
        or "http://localhost:3030/museum/data"
    )

    parser = argparse.ArgumentParser(description="Unggah Turtle museum ke Fuseki.")
    parser.add_argument("--endpoint", default=bawaan, help="URL Graph Store Fuseki")
    parser.add_argument("--berkas", default=str(DATA), help="Berkas Turtle sumber")
    args = parser.parse_args()

    berkas = Path(args.berkas)
    if not berkas.exists():
        print(
            f"Berkas tidak ditemukan: {berkas}\n"
            "Jalankan `python scripts/generate.py` lebih dulu.",
            file=sys.stderr,
        )
        return 1

    isi = berkas.read_bytes()
    print(f"Mengunggah {berkas.name} ({len(isi) / 1024:.1f} KB) ke {args.endpoint}")
    try:
        unggah(args.endpoint, isi)
    except urllib.error.URLError as exc:
        print(
            "Tidak dapat terhubung ke Fuseki.\n"
            f"  Endpoint : {args.endpoint}\n"
            f"  Penyebab : {exc.reason}\n"
            "Pastikan Fuseki berjalan dan dataset bernama `museum` sudah dibuat. "
            "Panduan lengkap ada di docs/fuseki-setup.md.",
            file=sys.stderr,
        )
        return 1
    except RuntimeError as exc:
        print(f"Gagal mengunggah: {exc}", file=sys.stderr)
        return 1

    print("Selesai. Graph default Fuseki kini berisi data museum yang baru.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
