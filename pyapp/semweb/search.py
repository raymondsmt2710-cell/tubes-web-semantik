"""Pencarian semantik dengan SPARQL SELECT.

Aturan yang dipegang modul ini:

- Semua penyaringan dilakukan **di dalam SPARQL**, bukan dengan menyaring list
  di Python sesudah query. Ini aturan materi P9/P10 dan juga alasan hasilnya
  bisa dipindah ke Fuseki tanpa berubah arti.
- `PREFIX` selalu ditulis lengkap di dalam string query, walau editor seperti
  WDQS menyuntikkannya otomatis.
- Kata kunci pengguna tidak pernah disambung mentah ke dalam query; lihat
  `_bersihkan_kata`.
"""

from __future__ import annotations

import re
from typing import Any

from rdflib import URIRef
from rdflib.namespace import RDF

from .namespace import RES, SDP
from .store import MuseumStore

PREFIXES = """PREFIX sdp:  <https://museumsumatera.id/ontology#>
PREFIX res:  <https://museumsumatera.id/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX geo:  <http://www.w3.org/2003/01/geo/wgs84_pos#>
"""

# Karakter yang bisa mengubah struktur query bila lolos ke dalam string SPARQL.
_BERBAHAYA = re.compile(r'["\\{};<>]|\bUNION\b|\bINSERT\b|\bDELETE\b', re.IGNORECASE)


def _bersihkan_kata(teks: str) -> list[str]:
    """Pecah teks menjadi kata yang aman dipakai di dalam FILTER.

    Kata yang memuat karakter struktural SPARQL dibuang seluruhnya, sehingga
    upaya menyuntikkan klausa berakhir sebagai pencarian kosong — bukan query
    yang rusak dan bukan error 500.
    """
    if not teks:
        return []
    kata: list[str] = []
    for bagian in teks.split():
        if _BERBAHAYA.search(bagian):
            continue
        bersih = bagian.strip().strip("\"'")
        if bersih:
            kata.append(bersih)
    return kata


def _literal(teks: str) -> str:
    """Bungkus teks sebagai literal SPARQL yang aman."""
    aman = teks.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{aman}"'


def kueri_cari(
    q: str | None = None,
    provinsi: str | None = None,
    tema: str | None = None,
    era: str | None = None,
    tahun_min: int | None = None,
    urut: str | None = None,
    batas: int = 300,
) -> str:
    """Susun query SELECT pencarian museum.

    Setiap kata pada `q` harus muncul di salah satu bidang yang dicari, jadi
    "museum aceh" dan "medan" sama-sama bisa menemukan museum yang tepat.
    """
    pola = [
        "  ?museum a sdp:Museum ;",
        "          sdp:name ?nama .",
        "  OPTIONAL { ?museum sdp:locatedInCity ?kotaNode . ?kotaNode sdp:name ?kota . }",
        "  OPTIONAL { ?museum sdp:locatedInProvince ?provNode . ?provNode sdp:name ?provinsi . }",
        "  OPTIONAL { ?museum sdp:hasTheme ?temaNode . ?temaNode sdp:name ?tema . }",
        "  OPTIONAL { ?museum sdp:hasEra ?eraNode . ?eraNode sdp:name ?era . }",
        "  OPTIONAL { ?museum sdp:establishedYear ?tahun . }",
        "  OPTIONAL { ?museum sdp:description ?deskripsi . }",
    ]

    filter_baris: list[str] = []
    if provinsi:
        filter_baris.append(f"  FILTER(LCASE(STR(?provinsi)) = LCASE({_literal(provinsi)}))")
    if tema:
        filter_baris.append(f"  FILTER(LCASE(STR(?tema)) = LCASE({_literal(tema)}))")
    if era:
        filter_baris.append(f"  FILTER(LCASE(STR(?era)) = LCASE({_literal(era)}))")
    if tahun_min is not None:
        filter_baris.append("  FILTER(BOUND(?tahun) && xsd:integer(STR(?tahun)) >= %d)" % tahun_min)

    for kata in _bersihkan_kata(q or ""):
        literal = _literal(kata)
        filter_baris.append(
            "  FILTER(\n"
            f"    CONTAINS(LCASE(STR(?nama)), LCASE({literal})) ||\n"
            f"    CONTAINS(LCASE(COALESCE(STR(?kota), '')), LCASE({literal})) ||\n"
            f"    CONTAINS(LCASE(COALESCE(STR(?provinsi), '')), LCASE({literal})) ||\n"
            f"    CONTAINS(LCASE(COALESCE(STR(?tema), '')), LCASE({literal})) ||\n"
            f"    CONTAINS(LCASE(COALESCE(STR(?era), '')), LCASE({literal})) ||\n"
            f"    CONTAINS(LCASE(COALESCE(STR(?deskripsi), '')), LCASE({literal}))\n"
            "  )"
        )

    urutan = {
        "nama": "ORDER BY LCASE(STR(?nama))",
        "tahun": "ORDER BY COALESCE(xsd:integer(STR(?tahun)), 0)",
    }.get(urut or "", "ORDER BY LCASE(STR(?nama))")

    badan = "\n".join(pola + filter_baris)
    return (
        f"{PREFIXES}\n"
        "SELECT ?museum ?nama ?kota ?provinsi ?tema ?era ?tahun ?deskripsi\n"
        "WHERE {\n"
        f"{badan}\n"
        "}\n"
        f"{urutan}\n"
        f"LIMIT {max(1, int(batas))}\n"
    )


def _slug(subjek: URIRef) -> str:
    return str(subjek).rsplit("/", 1)[-1]


def cari_museum(
    store: MuseumStore,
    q: str | None = None,
    provinsi: str | None = None,
    tema: str | None = None,
    era: str | None = None,
    tahun_min: int | None = None,
    urut: str | None = None,
    batas: int = 300,
) -> list[dict[str, Any]]:
    """Jalankan pencarian dan kembalikan hasil siap dipakai UI.

    Museum yang punya beberapa tema muncul lebih dari sekali di hasil SPARQL;
    di sini barisnya digabung per museum agar daftar tetap satu baris per
    museum.
    """
    query = kueri_cari(q, provinsi, tema, era, tahun_min, urut, batas)
    hasil: dict[str, dict[str, Any]] = {}

    for baris in store.closure.query(query):
        museum = baris[0]
        if museum is None:
            continue
        kunci = str(museum)
        entri = hasil.get(kunci)
        if entri is None:
            entri = {
                "uri": kunci,
                "slug": _slug(museum),
                "nama": str(baris[1]) if baris[1] is not None else "",
                "kota": str(baris[2]) if baris[2] is not None else None,
                "provinsi": str(baris[3]) if baris[3] is not None else None,
                "tema": [],
                "era": str(baris[5]) if baris[5] is not None else None,
                "tahun": None,
                "deskripsi": str(baris[7]) if baris[7] is not None else None,
            }
            hasil[kunci] = entri

        if baris[4] is not None and str(baris[4]) not in entri["tema"]:
            entri["tema"].append(str(baris[4]))
        if entri["tahun"] is None and baris[6] is not None:
            mentah = str(baris[6])
            try:
                entri["tahun"] = int(mentah)
            except ValueError:
                entri["tahun"] = None

    daftar = list(hasil.values())
    for entri in daftar:
        entri["tema"].sort()
    return daftar


def daftar_provinsi(store: MuseumStore) -> list[str]:
    """Nama provinsi unik yang terpakai di graf, terurut abjad."""
    return _nilai_per_kelas(store, SDP.Province)


def daftar_tema(store: MuseumStore) -> list[str]:
    """Nama tema unik yang terpakai di graf, terurut abjad."""
    return _nilai_per_kelas(store, SDP.Theme)


def daftar_era(store: MuseumStore) -> list[str]:
    """Nama era unik yang terpakai di graf, terurut abjad."""
    return _nilai_per_kelas(store, SDP.Era)


def _nilai_per_kelas(store: MuseumStore, kelas) -> list[str]:
    """Ambil semua `sdp:name` milik node bertipe `kelas`."""
    nilai = {
        str(label)
        for node in store.asserted.subjects(RDF.type, kelas)
        for label in store.asserted.objects(node, SDP.name)
        if label is not None
    }
    return sorted(nilai)
