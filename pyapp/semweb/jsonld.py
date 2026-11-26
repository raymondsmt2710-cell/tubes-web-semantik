"""JSON-LD dengan kosakata schema.org (materi P3: JSON-LD & structured data).

Graf proyek memakai kosakata sendiri (``sdp:``). Mesin pencari tidak mengenal
``sdp:``; mereka membaca ``schema.org``. Modul ini memetakan satu museum dari
graf ke dokumen JSON-LD ``schema:Museum`` sehingga data yang **sama** bisa
dibaca mesin di luar proyek.

Pemetaan yang dipakai:

=====================  ==========================================
graf (``sdp:``)        JSON-LD (``schema.org``)
=====================  ==========================================
``sdp:name``           ``name``
``sdp:description``    ``description``
``sdp:address``        ``address.streetAddress``
kota / provinsi        ``address.addressLocality`` / ``addressRegion``
``sdp:latitude``       ``geo.latitude``
``sdp:longitude``      ``geo.longitude``
``sdp:establishedYear````foundingDate``
``sdp:openingHours``   ``openingHours``
``sdp:officialUrl``    ``sameAs``
``sdp:hasImage``       ``image`` (URL absolut, urut ``imageIndex``)
=====================  ==========================================

Aturan yang dipegang:

- Data diambil lewat SPARQL SELECT, sama seperti modul domain lain.
- Bidang yang tidak ada di graf **dihilangkan**, bukan diisi ``null`` —
  validator schema.org menganggap ``null`` sebagai nilai yang salah.
"""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urljoin

from rdflib import Graph, Namespace, URIRef

from .namespace import RES
from .sparql import NAMA, PREFIXES
from .store import MuseumStore

SCHEMA = Namespace("https://schema.org/")

# Konteks resmi ("https://schema.org") butuh unduhan jaringan saat di-parse.
# Untuk test dan pemeriksaan round-trip, konteks setara dipakai secara lokal.
KONTEKS_OFFLINE = {"@vocab": str(SCHEMA)}

_SLUG_SAH = re.compile(r"^[a-z0-9][a-z0-9-]{0,119}$")

__all__ = ["SCHEMA", "ke_graf", "museum_jsonld", "semua_museum_jsonld"]


def _kueri_museum(iri: URIRef) -> str:
    return (
        f"{PREFIXES}\n"
        "SELECT ?nama ?deskripsi ?alamat ?kota ?provinsi ?lat ?lng ?tahun ?jam ?resmi\n"
        "WHERE {\n"
        f"  VALUES ?museum {{ <{iri}> }}\n"
        f"  ?museum a sdp:Museum ; {NAMA} ?nama .\n"
        "  OPTIONAL { ?museum sdp:description ?deskripsi . }\n"
        "  OPTIONAL { ?museum sdp:address ?alamat . }\n"
        f"  OPTIONAL {{ ?museum sdp:locatedInCity ?k . ?k {NAMA} ?kota . }}\n"
        f"  OPTIONAL {{ ?museum sdp:locatedInProvince ?p . ?p {NAMA} ?provinsi . }}\n"
        "  OPTIONAL { ?museum sdp:latitude ?lat ; sdp:longitude ?lng . }\n"
        "  OPTIONAL { ?museum sdp:establishedYear ?tahun . }\n"
        "  OPTIONAL { ?museum sdp:openingHours ?jam . }\n"
        "  OPTIONAL { ?museum sdp:officialUrl ?resmi . }\n"
        "}\n"
        "LIMIT 1\n"
    )


def _kueri_gambar(iri: URIRef) -> str:
    return (
        f"{PREFIXES}\n"
        "SELECT ?url\n"
        "WHERE {\n"
        f"  <{iri}> sdp:hasImage ?img .\n"
        "  ?img sdp:imageUrl ?url .\n"
        "  OPTIONAL { ?img sdp:imageIndex ?urut . }\n"
        "}\n"
        "ORDER BY COALESCE(?urut, 0)\n"
        "LIMIT 50\n"
    )


def _kueri_semua() -> str:
    return (
        f"{PREFIXES}\n"
        "SELECT ?museum ?nama\n"
        "WHERE {\n"
        f"  ?museum a sdp:Museum ; {NAMA} ?nama .\n"
        "}\n"
        "ORDER BY LCASE(STR(?nama))\n"
        "LIMIT 500\n"
    )


def _absolut(basis: str, jalur: str) -> str:
    """Gambar disimpan relatif (``/images/...``); schema.org butuh URL penuh."""
    return urljoin(basis if basis.endswith("/") else basis + "/", jalur)


def _tahun(nilai: Any) -> str | None:
    """``foundingDate`` menerima tahun ISO 8601; ambil empat digit pertama.

    Dengan begitu data berbentuk ``"1915-01-01"`` pun tetap menjadi ``"1915"``.
    """
    teks = str(nilai).strip()[:4]
    return teks if teks.isdigit() else None


def _dari_iri(store: MuseumStore, iri: URIRef, basis: str) -> dict[str, Any] | None:
    baris = next(iter(store.closure.query(_kueri_museum(iri))), None)
    if baris is None:
        return None
    nama, deskripsi, alamat, kota, provinsi, lat, lng, tahun, jam, resmi = baris
    slug = str(iri).rsplit("/", 1)[-1]

    doc: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Museum",
        "@id": str(iri),
        "name": str(nama),
        "url": _absolut(basis, f"museum/{slug}"),
    }
    if deskripsi is not None:
        doc["description"] = str(deskripsi)

    alamat_doc = {
        kunci: str(nilai)
        for kunci, nilai in (
            ("streetAddress", alamat),
            ("addressLocality", kota),
            ("addressRegion", provinsi),
        )
        if nilai is not None
    }
    if alamat_doc:
        doc["address"] = {"@type": "PostalAddress", **alamat_doc, "addressCountry": "ID"}

    if lat is not None and lng is not None:
        doc["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": float(lat),
            "longitude": float(lng),
        }

    if tahun is not None and (teks_tahun := _tahun(tahun)):
        doc["foundingDate"] = teks_tahun
    if jam is not None:
        doc["openingHours"] = str(jam)
    if resmi is not None:
        doc["sameAs"] = str(resmi)

    gambar = [
        _absolut(basis, str(b[0]))
        for b in store.closure.query(_kueri_gambar(iri))
        if b[0] is not None
    ]
    if gambar:
        doc["image"] = gambar
    return doc


def museum_jsonld(store: MuseumStore, slug: str, basis: str) -> dict[str, Any] | None:
    """Dokumen JSON-LD satu museum, atau ``None`` bila slug tidak sah/tidak ada.

    ``basis`` adalah URL situs (mis. ``https://museum.example/``) untuk
    menyusun ``url`` dan ``image`` absolut.
    """
    if not slug or not _SLUG_SAH.match(slug):
        return None
    return _dari_iri(store, URIRef(f"{RES}museum/{slug}"), basis)


def semua_museum_jsonld(store: MuseumStore, basis: str) -> dict[str, Any]:
    """Seluruh museum sebagai satu dokumen ``@graph`` (untuk ekspor/unduhan)."""
    graf = []
    for baris in store.closure.query(_kueri_semua()):
        doc = _dari_iri(store, URIRef(baris[0]), basis)
        if doc is not None:
            doc.pop("@context", None)
            graf.append(doc)
    return {"@context": "https://schema.org", "@graph": graf}


def ke_graf(doc: dict[str, Any]) -> Graph:
    """Parse JSON-LD kembali menjadi graf RDF tanpa akses jaringan.

    Dipakai untuk membuktikan round-trip: properti yang dipetakan harus kembali
    dengan nilai yang sama seperti di graf asal.
    """
    salinan = dict(doc)
    salinan["@context"] = KONTEKS_OFFLINE
    g = Graph()
    g.parse(data=json.dumps(salinan), format="json-ld")
    return g
