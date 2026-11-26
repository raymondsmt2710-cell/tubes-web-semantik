"""Benang merah antar museum memakai CONSTRUCT dan property path.

Materi P11 menekankan bahwa hasil query tidak harus tabel: CONSTRUCT
mengembalikan **graf baru**. Modul ini memakai CONSTRUCT untuk menghitung bobot
relasi antar museum di dalam SPARQL, bukan di Python, lalu menelusuri tetangga
dengan property path untuk kebutuhan GraphRAG.
"""

from __future__ import annotations

from typing import Any

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import OWL, RDFS

from .namespace import RES, SDP
from .store import MuseumStore

PREFIXES = """PREFIX sdp:  <https://museumsumatera.id/ontology#>
PREFIX res:  <https://museumsumatera.id/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
"""

# Objek yang tidak informatif dan hanya memperbesar konteks.
TRIVIAL = {OWL.Thing, RDFS.Resource, OWL.NamedIndividual}


def kueri_benang_merah(slug: str, maks: int = 6) -> str:
    """Susun query CONSTRUCT yang menghitung bobot relasi ke museum lain.

    Bobot mengikuti aturan yang sudah dipakai data lama: tema sama +3 per tema,
    relasi arsip eksplisit +4, kota sama +2, era sama +1, bab bersebelahan +1.
    Semua perhitungan terjadi di dalam SPARQL.
    """
    diri = f"<{RES}museum/{slug}>"
    return f"""{PREFIXES}
CONSTRUCT {{ ?lain sdp:bobotRelasi ?skor }}
WHERE {{
  {diri} sdp:chapter ?babDiri .
  ?babDiri sdp:chapterIndex ?idxDiri .

  ?lain a sdp:Museum .
  FILTER(?lain != {diri})

  OPTIONAL {{ {diri} sdp:relatedMuseum ?lain . BIND(4 AS ?bArsip) }}

  {{
    SELECT ?lain (COUNT(DISTINCT ?tema) * 3 AS ?bTema)
    WHERE {{
      {diri} sdp:hasTheme ?tema .
      ?lain  sdp:hasTheme ?tema .
      FILTER(?lain != {diri})
    }}
    GROUP BY ?lain
  }}

  OPTIONAL {{
    {diri} sdp:locatedInCity ?kota .
    ?lain  sdp:locatedInCity ?kota .
    BIND(2 AS ?bKota)
  }}

  OPTIONAL {{
    {diri} sdp:hasEra ?era .
    ?lain  sdp:hasEra ?era .
    BIND(1 AS ?bEra)
  }}

  OPTIONAL {{
    ?lain sdp:chapter ?babLain .
    ?babLain sdp:chapterIndex ?idxLain .
    FILTER(ABS(xsd:integer(STR(?idxLain)) - xsd:integer(STR(?idxDiri))) = 1)
    BIND(1 AS ?bBab)
  }}

  BIND(COALESCE(?bArsip, 0) + COALESCE(?bTema, 0) + COALESCE(?bKota, 0)
       + COALESCE(?bEra, 0) + COALESCE(?bBab, 0) AS ?skor)
  FILTER(?skor > 0)
}}
LIMIT {max(1, int(maks))}
"""


def _alasan(store: MuseumStore, diri: str, lain: str) -> str:
    """Susun alasan dari relasi yang benar-benar cocok, bukan dari tebakan."""
    a = URIRef(f"{RES}museum/{diri}")
    b = URIRef(f"{RES}museum/{lain}")
    bagian: list[str] = []

    tema_a = {t for t in store.asserted.objects(a, SDP.hasTheme)}
    tema_b = {t for t in store.asserted.objects(b, SDP.hasTheme)}
    sama = tema_a & tema_b
    if sama:
        nama = ", ".join(sorted(store.nama(t) for t in sama))
        bagian.append(f"tema sama ({nama})")

    if (a, SDP.relatedMuseum, b) in store.asserted:
        bagian.append("relasi arsip eksplisit")

    kota_a = set(store.asserted.objects(a, SDP.locatedInCity))
    kota_b = set(store.asserted.objects(b, SDP.locatedInCity))
    if kota_a & kota_b:
        bagian.append(f"kota sama ({store.nama(next(iter(kota_a & kota_b)))})")

    era_a = set(store.asserted.objects(a, SDP.hasEra))
    era_b = set(store.asserted.objects(b, SDP.hasEra))
    if era_a & era_b:
        bagian.append(f"era sama ({store.nama(next(iter(era_a & era_b)))})")

    idx_a = store.asserted.value(a, SDP.chapterIndex)
    idx_b = store.asserted.value(b, SDP.chapterIndex)
    if idx_a is None:
        # chapterIndex melekat pada node bab, bukan museum.
        bab_a = store.asserted.value(a, SDP.chapter)
        idx_a = store.asserted.value(bab_a, SDP.chapterIndex) if bab_a else None
    if idx_b is None:
        bab_b = store.asserted.value(b, SDP.chapter)
        idx_b = store.asserted.value(bab_b, SDP.chapterIndex) if bab_b else None
    if idx_a is not None and idx_b is not None:
        if abs(int(idx_a) - int(idx_b)) == 1:
            bagian.append("bab bersebelahan")

    return " · ".join(bagian) if bagian else "relasi lemah"


def benang_merah(store: MuseumStore, slug: str, maks: int = 6) -> list[dict[str, Any]]:
    """Kembalikan museum lain yang berhubungan, beserta skor dan alasannya."""
    query = kueri_benang_merah(slug, maks)
    hasil_graf: Graph = store.closure.query(query, initNs={"sdp": SDP, "res": RES})

    hasil: list[dict[str, Any]] = []
    for subjek, _, skor in hasil_graf:
        if not isinstance(subjek, URIRef):
            continue
        lain = str(subjek).rsplit("/", 1)[-1]
        nilai = int(skor) if isinstance(skor, Literal) else 0
        hasil.append(
            {
                "uri": str(subjek),
                "slug": lain,
                "nama": store.nama(subjek),
                "skor": nilai,
                "alasan": _alasan(store, slug, lain),
            }
        )

    hasil.sort(key=lambda h: (-h["skor"], h["nama"].lower()))
    return hasil[:maks]


def _tetangga(store: MuseumStore, node: URIRef, arah: str) -> set[URIRef]:
    """Node yang terhubung satu langkah dari `node` pada arah tertentu."""
    hasil: set[URIRef] = set()
    if arah in ("keluar", "keduanya"):
        for _, _, objek in store.closure.triples((node, None, None)):
            if isinstance(objek, URIRef) and objek not in TRIVIAL:
                hasil.add(objek)
    if arah in ("masuk", "keduanya"):
        for subjek, _, _ in store.closure.triples((None, None, node)):
            if isinstance(subjek, URIRef) and subjek not in TRIVIAL:
                hasil.add(subjek)
    return hasil


def subgraf_sekitar(store: MuseumStore, slug: str, hop: int = 1) -> Graph:
    """Ambil triple di sekitar satu museum hingga `hop` langkah.

    Ini pola retrieval GraphRAG pada materi P13: dari satu jangkar, telusuri
    tetangga, lalu kirim hanya subgraf itu sebagai konteks — bukan seluruh graf.
    """
    akar = URIRef(f"{RES}museum/{slug}")
    g = Graph()
    for prefix, ns in (("sdp", SDP), ("res", RES)):
        g.bind(prefix, ns)

    dikunjungi = {akar}
    batas = {akar}
    for _ in range(max(0, hop)):
        berikut: set[URIRef] = set()
        for node in batas:
            for tetangga in _tetangga(store, node, "keduanya"):
                if tetangga not in dikunjungi:
                    berikut.add(tetangga)
        dikunjungi |= berikut
        batas = berikut
        if not batas:
            break

    for node in dikunjungi:
        for s, p, o in store.closure.triples((node, None, None)):
            if isinstance(o, BNode):
                continue
            if o in TRIVIAL:
                continue
            if o == s:
                continue
            if isinstance(o, URIRef) and o not in dikunjungi:
                # Sertakan triple penghubung tapi bukan isi node yang jauh.
                g.add((s, p, o))
                continue
            g.add((s, p, o))

    return g
