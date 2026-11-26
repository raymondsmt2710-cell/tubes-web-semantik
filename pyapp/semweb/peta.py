"""Koordinat museum untuk halaman peta (tugas D3).

Lintang dan bujur sudah ada di graf (``sdp:latitude``, ``sdp:longitude``).
Modul ini hanya mengambilnya lewat SPARQL SELECT; saringan provinsi ditulis
**di dalam** query (aturan P9/P10), bukan dengan menyaring list di Python.
"""

from __future__ import annotations

from typing import Any

from .sparql import NAMA, PREFIXES
from .sparql import literal as _literal
from .store import MuseumStore

__all__ = ["kueri_peta", "titik_museum"]


def kueri_peta(provinsi: str | None = None, batas: int = 500) -> str:
    """Query SELECT museum beserta koordinatnya, opsional per provinsi.

    Koordinat dibuat OPTIONAL: museum tanpa koordinat tetap muncul di daftar
    (dengan keterangan), hanya tidak menjadi penanda di peta.
    """
    saring = ""
    if provinsi and provinsi.strip():
        saring = f"  FILTER(LCASE(STR(?provinsi)) = LCASE({_literal(provinsi.strip())}))\n"
    return (
        f"{PREFIXES}\n"
        "SELECT ?museum ?nama ?kota ?provinsi ?lat ?lng\n"
        "WHERE {\n"
        f"  ?museum a sdp:Museum ; {NAMA} ?nama .\n"
        f"  OPTIONAL {{ ?museum sdp:locatedInCity ?k . ?k {NAMA} ?kota . }}\n"
        f"  OPTIONAL {{ ?museum sdp:locatedInProvince ?p . ?p {NAMA} ?provinsi . }}\n"
        "  OPTIONAL { ?museum sdp:latitude ?lat ; sdp:longitude ?lng . }\n"
        f"{saring}"
        "}\n"
        "ORDER BY LCASE(STR(?nama))\n"
        f"LIMIT {max(1, int(batas))}\n"
    )


def _angka(nilai: Any) -> float | None:
    if nilai is None:
        return None
    try:
        return float(nilai)
    except (TypeError, ValueError):
        return None


def titik_museum(store: MuseumStore, provinsi: str | None = None) -> list[dict[str, Any]]:
    """Daftar museum ``{slug, nama, kota, provinsi, lat, lng}`` terurut nama."""
    hasil: dict[str, dict[str, Any]] = {}
    for museum, nama, kota, prov, lat, lng in store.closure.query(kueri_peta(provinsi)):
        kunci = str(museum)
        if kunci in hasil:
            # Label ganda (sdp:name dan rdfs:label) menghasilkan baris ganda.
            continue
        hasil[kunci] = {
            "slug": kunci.rsplit("/", 1)[-1],
            "nama": str(nama),
            "kota": str(kota) if kota is not None else None,
            "provinsi": str(prov) if prov is not None else None,
            "lat": _angka(lat),
            "lng": _angka(lng),
        }
    return list(hasil.values())
