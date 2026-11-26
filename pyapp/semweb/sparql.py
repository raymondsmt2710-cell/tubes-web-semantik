"""Perkakas SPARQL yang dipakai bersama seluruh modul.

Materi P9 dan P10 memberi tiga aturan yang dipegang di sini:

1. ``PREFIX`` selalu ditulis lengkap di dalam string query, walau editor
   seperti WDQS menyuntikkannya otomatis. Dengan begitu query yang sama bisa
   dipindah ke Fuseki atau ke ``rdflib`` tanpa diubah.
2. Kata kunci pengguna tidak pernah disambung mentah ke dalam query.
3. Nilai literal selalu di-escape sebelum masuk query.
"""

from __future__ import annotations

import re

from .namespace import RES, SDP

# PREFIX ditulis tangan, bukan disuntikkan editor.
PREFIXES = f"""PREFIX sdp:  <{SDP}>
PREFIX res:  <{RES}>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX geo:  <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
"""

# Prefiks yang dikenali saat memeriksa IRI di guard (P13).
PREFIX_MAP: dict[str, str] = {
    "sdp": str(SDP),
    "res": str(RES),
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "dct": "http://purl.org/dc/terms/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
}

# Karakter struktural yang bisa mengubah bentuk query bila lolos sebagai kata.
_BERBAHAYA = re.compile(
    r'["\\{}<>]|\bUNION\b|\bINSERT\b|\bDELETE\b|\bDROP\b|\bLOAD\b', re.IGNORECASE
)

# Pola "nama entitas". Dua jalur data yang sah dipakai proyek ini: generator
# Python menulis ``sdp:name``, sedangkan generator RDF/XML menulis
# ``rdfs:label``. Kueri harus menerima keduanya supaya hasil tidak kosong hanya
# karena data dimuat dari pipeline yang berbeda. Jalur alternatif ``|`` dipilih
# (bukan UNION) agar polanya tetap satu.
NAMA = "(sdp:name|rdfs:label)"


def bersihkan_kata(teks: str | None) -> list[str]:
    """Pecah teks pengguna menjadi kata yang aman dipakai di dalam ``FILTER``.

    Kata yang memuat karakter struktural SPARQL dibuang seluruhnya, sehingga
    upaya menyuntikkan klausa berakhir sebagai pencarian kosong — bukan query
    rusak dan bukan error 500.
    """
    if not teks:
        return []
    hasil: list[str] = []
    for bagian in teks.split():
        if _BERBAHAYA.search(bagian):
            continue
        bersih = bagian.strip().strip("\"'")
        if bersih:
            hasil.append(bersih)
    return hasil


def literal(teks: str) -> str:
    """Bungkus teks sebagai literal SPARQL yang aman (kutip ganda)."""
    aman = str(teks).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{aman}"'


def iri_res(jenis: str, nama: str) -> str:
    """IRI resource di namespace ``res:``, mis. ``res:museum/museum-negeri-aceh``."""
    return f"<{RES}{jenis}/{nama}>"


def label_slug(iri: str) -> str:
    """Ambil bagian terakhir sebuah IRI: ``…/museum/x`` -> ``x``."""
    return str(iri).rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1]
