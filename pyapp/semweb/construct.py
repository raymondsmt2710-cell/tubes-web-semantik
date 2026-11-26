"""Hierarki kelas dan CONSTRUCT — bahan Pertemuan 11.

Materi P11 memberi tiga pelajaran yang dipakai modul ini:

1. ``CONSTRUCT`` mencetak template sekali per *solution*, sedangkan graf
   adalah **himpunan** — cetakan kembar tersimpan sekali. Karena itu jumlah
   triple hasil CONSTRUCT jarang sama dengan jumlah baris ``SELECT``.
2. ``rdfs:subClassOf`` bisa ditelusuri dengan operator jalur: ``+`` satu
   langkah atau lebih, ``*`` nol langkah atau lebih.
3. Hasil penelusuran hierarki bisa **dimaterialisasi** menjadi triple baru.
   Yang kita tulis dengan tangan di P11 setara aturan ``rdfs9`` dan ``rdfs11``;
   di P12 mesin (``owlrl``) yang menjalankannya sendiri.
"""

from __future__ import annotations

from typing import Any

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

from .namespace import SDP
from .sparql import PREFIX_MAP, PREFIXES, bersihkan_kata
from .store import MuseumStore

__all__ = [
    "hierarki_kelas",
    "kueri_hierarki",
    "kueri_materialisasi",
    "materialisasi",
    "selisih_construct_select",
    "subkelas_museum",
    "verifikasi_hierarki",
]

# Namespace awal untuk query(..., initNs=...). rdflib butuh objek Namespace,
# bukan string, agar prefiks di dalam string query dikenali.
INIT_NS = {k: Namespace(v) for k, v in PREFIX_MAP.items()}


def kueri_hierarki(kelas_induk: str = "Museum", operator: str = "+") -> str:
    """Query ``SELECT`` yang menelusuri subkelas dengan property path."""
    if operator not in ("+", "*"):
        raise ValueError("Operator jalur hanya '+' atau '*' (lihat materi P11).")
    if not bersihkan_kata(kelas_induk):
        raise ValueError("Nama kelas tidak boleh kosong.")
    return f"""{PREFIXES}
SELECT DISTINCT ?kelas ?nama WHERE {{
  ?kelas rdfs:subClassOf{operator} sdp:{kelas_induk} .
  OPTIONAL {{ ?kelas rdfs:label ?nama . }}
}}
ORDER BY ?kelas
"""


def hierarki_kelas(
    store: MuseumStore, kelas_induk: str = "Museum", operator: str = "+"
) -> list[dict[str, Any]]:
    """Daftar subkelas ``kelas_induk`` beserta labelnya."""
    hasil: list[dict[str, Any]] = []
    for baris in store.asserted.query(kueri_hierarki(kelas_induk, operator)):
        kelas, nama = baris[0], baris[1]
        if not isinstance(kelas, URIRef):
            continue
        hasil.append(
            {
                "uri": str(kelas),
                "nama": str(nama) if nama is not None else str(kelas).rsplit("#", 1)[-1],
                "lokal": str(kelas).rsplit("#", 1)[-1],
            }
        )
    hasil.sort(key=lambda h: h["lokal"].lower())
    return hasil


def subkelas_museum(store: MuseumStore) -> list[dict[str, Any]]:
    """Pintasan: subkelas langsung ``sdp:Museum`` (operator ``+``)."""
    return hierarki_kelas(store, "Museum", "+")


def kueri_materialisasi() -> str:
    """Query ``CONSTRUCT`` yang menurunkan tipe superkelas untuk setiap individu.

    Aturannya sama dengan yang ditulis tangan di P11: bila ``?x`` bertipe kelas
    ``K`` dan ``K`` subkelas dari ``?super`` sedalam apa pun, maka ``?x`` juga
    bertipe ``?super``. Ini setara ``rdfs9`` + ``rdfs11``.
    """
    return f"""{PREFIXES}
CONSTRUCT {{ ?x a ?super . }}
WHERE {{
  ?x a ?kelas .
  ?kelas rdfs:subClassOf+ ?super .
  FILTER(?kelas != ?super)
}}
"""


def _graf_dari_hasil(hasil: Any) -> Graph:
    """Ambil ``Graph`` dari hasil query CONSTRUCT rdflib.

    ``Graph.query`` mengembalikan ``Result``, bukan ``Graph``. Grafnya ada di
    ``Result.graph``; jangan diuji dengan ``or`` karena graf kosong tetap graf
    yang sah.
    """
    g = Graph()
    g.bind("sdp", SDP)
    graf = getattr(hasil, "graph", None)
    if graf is not None:
        for triple in graf:
            g.add(triple)
    else:
        for triple in hasil:
            g.add(triple)
    return g


def materialisasi(store: MuseumStore) -> tuple[Graph, dict[str, int]]:
    """Jalankan aturan materialisasi di atas graf asserted.

    Mengembalikan graf turunan dan angka pembanding: berapa triple yang
    dicetak CONSTRUCT, berapa yang **sudah ada** di graf asserted (cetakan
    kembar), dan berapa yang benar-benar baru.
    """
    hasil = store.asserted.query(kueri_materialisasi(), initNs=INIT_NS)
    turunan = _graf_dari_hasil(hasil)
    dicetak = len(turunan)
    sudah = sum(1 for t in turunan if t in store.asserted)
    baru = dicetak - sudah
    return turunan, {"dicetak": dicetak, "sudah_ada": sudah, "baru": baru}


def selisih_construct_select(
    store: MuseumStore, kueri_select: str, kueri_construct: str
) -> dict[str, int]:
    """Bandingkan jumlah baris ``SELECT`` dengan jumlah triple ``CONSTRUCT``."""
    baris = len(list(store.asserted.query(kueri_select, initNs=INIT_NS)))
    hasil = store.asserted.query(kueri_construct, initNs=INIT_NS)
    graf = _graf_dari_hasil(hasil)
    return {"baris_select": baris, "triple_construct": len(graf)}


def verifikasi_hierarki(store: MuseumStore) -> list[dict[str, Any]]:
    """Periksa apakah setiap subkelas museum benar-benar terpakai individu."""
    hasil: list[dict[str, Any]] = []
    for sub in subkelas_museum(store):
        kelas = URIRef(sub["uri"])
        jumlah = len(set(store.asserted.subjects(RDF.type, kelas)))
        hasil.append({**sub, "individu": jumlah})
    return hasil
