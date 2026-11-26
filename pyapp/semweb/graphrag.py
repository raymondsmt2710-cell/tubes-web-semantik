"""GraphRAG: mengambil subgraf dari Knowledge Graph sebagai konteks.

Materi P13 membedakan dua jenis retrieval:

- **Vector RAG** mengambil potongan teks yang mirip dengan pertanyaan. Ia tidak
  menelusuri relasi antar-fakta, sehingga pertanyaan multi-hop mudah gagal.
- **GraphRAG** mengambil **node, relasi, atau subgraf**. Satuannya fakta, bukan
  paragraf. Tiga pola retrieval-nya (P13 bagian 8):

  A. ``neighbors`` — semua triple keluar/masuk dari satu jangkar (1 hop).
  B. ``path`` — telusuri rantai relasi dengan property path ``+``/``*``.
  C. ``structured query`` — hasil ``SELECT`` dipakai sebagai konteks.

Aturan yang dipegang:

- Konteks diambil dari **closure** (asserted + inferred).
- Triple trivial dan triple refleksif dibuang.
- Jangkar dicari dari label/nama, bukan dari tebakan.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable

from rdflib import BNode, Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from .construct import INIT_NS
from .namespace import SDP
from .sparql import NAMA, PREFIXES, bersihkan_kata
from .store import MuseumStore

__all__ = [
    "KONTEKS",
    "PolaRetrieval",
    "ambil_konteks",
    "jangkar",
    "kueri_neighbors",
    "kueri_path",
    "pola_retrieval",
    "subgraf_hop",
    "triple_konteks",
]

# Objek yang tidak informatif dan hanya memperbesar konteks (P13, Demo A).
TRIVIAL: set[URIRef] = {OWL.Thing, RDFS.Resource, OWL.NamedIndividual}

# Batas aman supaya satu pertanyaan tidak menarik seluruh graf.
KONTEKS = 60


# --------------------------------------------------------------------- pola A


def kueri_neighbors(jangkar: URIRef, arah: str = "keluar") -> str:
    """Query ``CONSTRUCT`` pola *neighbors* (P13 pola A)."""
    subjek = f"<{jangkar}>"
    if arah == "keluar":
        pola = f"  {subjek} ?p ?o .\n  BIND({subjek} AS ?s)"
    elif arah == "masuk":
        pola = f"  ?s ?p {subjek} .\n  BIND({subjek} AS ?o)"
    elif arah == "keduanya":
        pola = (
            f"  {{ {subjek} ?p ?o . BIND({subjek} AS ?s) }}\n"
            "  UNION\n"
            f"  {{ ?s ?p {subjek} . BIND({subjek} AS ?o) }}"
        )
    else:
        raise ValueError("Arah hanya 'keluar', 'masuk', atau 'keduanya'.")
    return f"""{PREFIXES}
CONSTRUCT {{ ?s ?p ?o }}
WHERE {{
{pola}
}}
"""


# --------------------------------------------------------------------- pola B


def kueri_path(jangkar: URIRef, properti: str, operator: str = "+") -> str:
    """Query ``SELECT`` pola *path* (P13 pola B)."""
    if operator not in ("+", "*", ""):
        raise ValueError("Operator jalur hanya '+', '*', atau kosong.")
    if not bersihkan_kata(properti):
        raise ValueError("Nama properti tidak boleh kosong.")
    jalur = f"sdp:{properti}{operator}"
    return f"""{PREFIXES}
SELECT DISTINCT ?tujuan ?label WHERE {{
  <{jangkar}> {jalur} ?tujuan .
  OPTIONAL {{ ?tujuan {NAMA} ?label }}
}}
ORDER BY ?tujuan
"""


# --------------------------------------------------------------------- jangkar


@dataclass
class Jangkar:
    """Entitas jangkar yang ditemukan dari pertanyaan pengguna."""

    iri: URIRef
    label: str
    jenis: str

    def as_dict(self) -> dict[str, str]:
        return {"iri": str(self.iri), "label": self.label, "jenis": self.jenis}


def _memuat(teks: str, label: str) -> bool:
    """Apakah ``label`` muncul di ``teks`` sebagai kata utuh?

    Memakai batas kata supaya "era" tidak cocok di dalam "kamera" dan "Aceh"
    tidak cocok di dalam "Acehnese".
    """
    pola = r"(?<!\w)" + re.escape(label.lower()) + r"(?!\w)"
    return re.search(pola, teks) is not None


def jangkar(store: MuseumStore, pertanyaan: str, maks: int = 3) -> list[Jangkar]:
    """Temukan entitas jangkar yang disebut pada pertanyaan.

    Dua hal dijaga supaya jangkar tidak meleset:

    - **Label terpanjang menang.** "Museum Negeri Aceh" harus mengalahkan
      "Aceh" bila keduanya muncul, karena label panjang lebih spesifik.
    - **Batas kata.** Pencocokan memakai batas kata, bukan ``in`` biasa.
    """
    teks = (pertanyaan or "").strip().lower()
    if not teks:
        return []

    prioritas_jenis = {
        SDP.Museum: (0, "museum"),
        SDP.City: (1, "kota"),
        SDP.Province: (2, "provinsi"),
        SDP.Theme: (3, "tema"),
        SDP.Era: (4, "era"),
    }

    temuan: list[tuple[int, int, Jangkar]] = []
    sudah: set[str] = set()

    for kelas, (urutan, jenis) in prioritas_jenis.items():
        for node in store.asserted.subjects(RDF.type, kelas):
            if not isinstance(node, URIRef):
                continue
            label = store.nama(node)
            if not label or not _memuat(teks, label):
                continue
            if str(node) in sudah:
                continue
            sudah.add(str(node))
            temuan.append((-len(label), urutan, Jangkar(node, label, jenis)))

    temuan.sort(key=lambda t: (t[0], t[1]))
    return [j for _, _, j in temuan[:maks]]


# ------------------------------------------------------------------ subgraf


def _informatif(s: Any, p: Any, o: Any, akar: URIRef) -> bool:
    """Saring triple yang tidak menambah pengetahuan ke konteks."""
    if o in TRIVIAL or p in TRIVIAL:
        return False
    if isinstance(o, BNode):
        return False
    if s == o:  # triple refleksif hasil penalaran
        return False
    return True


def triple_konteks(
    store: MuseumStore,
    akar: Iterable[URIRef],
    hop: int = 1,
    batas: int = KONTEKS,
    mundur: bool = True,
) -> list[tuple[Any, Any, Any]]:
    """Ambil triple di sekitar satu atau beberapa jangkar hingga ``hop`` langkah.

    **Arah penelusuran penting.** Kalau jangkar adalah provinsi dan kita ikut
    menelusuri balik berulang kali, konteks akan menyedot seluruh museum di
    provinsi itu beserta semua foto dan detailnya. Karena itu:

    - Langkah **maju** dari jangkar boleh berulang sampai ``hop``.
    - Langkah **mundur** hanya satu langkah.
    """
    akar_bersih = [a for a in akar if isinstance(a, URIRef)]
    dikunjungi: set[URIRef] = set(akar_bersih)
    gelombang: set[URIRef] = set(akar_bersih)

    for putaran in range(max(0, int(hop))):
        berikut: set[URIRef] = set()
        for node in gelombang:
            for _, _, o in store.closure.triples((node, None, None)):
                if isinstance(o, URIRef) and o not in TRIVIAL and o not in dikunjungi:
                    berikut.add(o)
            if mundur and putaran == 0:
                for s, _, _ in store.closure.triples((None, None, node)):
                    if isinstance(s, URIRef) and s not in TRIVIAL and s not in dikunjungi:
                        berikut.add(s)
        if not berikut:
            break
        dikunjungi |= berikut
        gelombang = berikut
        mundur = False

    hasil: list[tuple[Any, Any, Any]] = []
    terlihat: set[tuple[Any, Any, Any]] = set()
    for node in dikunjungi:
        for s, p, o in store.closure.triples((node, None, None)):
            if not _informatif(s, p, o, node):
                continue
            if (s, p, o) in terlihat:
                continue
            terlihat.add((s, p, o))
            hasil.append((s, p, o))
            if len(hasil) >= batas:
                return hasil
    return hasil


def subgraf_hop(store: MuseumStore, akar: URIRef, hop: int = 1, batas: int = KONTEKS) -> Graph:
    """Bungkus ``triple_konteks`` menjadi ``Graph`` agar bisa diserialisasi."""
    g = Graph()
    g.bind("sdp", SDP)
    for triple in triple_konteks(store, [akar], hop, batas):
        g.add(triple)
    return g


# --------------------------------------------------------------- perakitan


@dataclass
class PolaRetrieval:
    """Jejak satu langkah retrieval, ditampilkan supaya sistem dapat diaudit."""

    pola: str
    keterangan: str
    query: str
    triple: list[str] = field(default_factory=list)
    baris: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "pola": self.pola,
            "keterangan": self.keterangan,
            "query": self.query,
            "jumlah_triple": len(self.triple),
            "baris": self.baris,
        }


def _n3(store: MuseumStore, triple: tuple[Any, Any, Any]) -> str:
    nm = store.asserted.namespace_manager
    return " ".join(x.n3(nm) for x in triple) + " ."


def pola_retrieval(
    store: MuseumStore,
    pertanyaan: str,
    hop: int = 1,
    properti_path: str = "partOfProvince",
    batas: int = KONTEKS,
) -> tuple[list[Jangkar], list[PolaRetrieval]]:
    """Jalankan tiga pola retrieval GraphRAG dan kembalikan jejaknya."""
    temuan = jangkar(store, pertanyaan)
    jejak: list[PolaRetrieval] = []

    if not temuan:
        return temuan, jejak

    akar = [j.iri for j in temuan]

    # Pola A — neighbors (CONSTRUCT, dua arah).
    q_neighbors = kueri_neighbors(akar[0], "keduanya")
    hasil_query = store.closure.query(q_neighbors, initNs=INIT_NS)
    graf = getattr(hasil_query, "graph", None)
    triple_neighbors = list(graf) if graf is not None else list(hasil_query)
    triple_bersih = [t for t in triple_neighbors if _informatif(t[0], t[1], t[2], akar[0])][
        :batas
    ]
    jejak.append(
        PolaRetrieval(
            pola="A · neighbors",
            keterangan=f"Triple masuk dan keluar dari {temuan[0].label} (1 hop, closure).",
            query=q_neighbors,
            triple=[_n3(store, t) for t in triple_bersih],
        )
    )

    # Pola B — path (property path dari jangkar kota/provinsi).
    target = temuan[0]
    if target.jenis in ("kota", "provinsi"):
        q_path = kueri_path(target.iri, properti_path, "+")
        baris_path = list(store.closure.query(q_path, initNs=INIT_NS))
        jejak.append(
            PolaRetrieval(
                pola="B · path",
                keterangan=f"Telusuri sdp:{properti_path}+ dari {target.label}.",
                query=q_path,
                baris=len(baris_path),
                triple=[f"{r[0]}  # {r[1]}" for r in baris_path],
            )
        )

    # Pola C — structured query: subgraf hop untuk seluruh jangkar.
    q_sub = kueri_neighbors(akar[0], "keduanya")
    triple_hop = triple_konteks(store, akar, hop=hop, batas=batas)
    jejak.append(
        PolaRetrieval(
            pola="C · structured query",
            keterangan=f"Konteks {len(akar)} jangkar hingga {hop} hop, dibatasi {batas} triple.",
            query=q_sub,
            triple=[_n3(store, t) for t in triple_hop],
        )
    )

    return temuan, jejak


def ambil_konteks(
    store: MuseumStore,
    pertanyaan: str,
    hop: int = 1,
    batas: int = KONTEKS,
) -> dict[str, Any]:
    """Konteks siap pakai untuk verbalisasi: jangkar, triple, dan teks konteks."""
    temuan = jangkar(store, pertanyaan)
    if not temuan:
        return {
            "ditemukan": False,
            "jangkar": [],
            "triple": [],
            "teks": "",
            "sumber": [],
            "jumlah_triple": 0,
        }

    triple = triple_konteks(store, [j.iri for j in temuan], hop=hop, batas=batas)
    teks = "\n".join(_n3(store, t) for t in triple)

    sumber = sorted(
        {
            str(x)
            for t in triple
            for x in t
            if isinstance(x, URIRef) and "/resource/" in str(x)
        }
    )

    return {
        "ditemukan": True,
        "jangkar": [j.as_dict() for j in temuan],
        "triple": [_n3(store, t) for t in triple],
        "teks": teks,
        "sumber": sumber,
        "jumlah_triple": len(triple),
    }


def iringan_label(store: MuseumStore, triple: Iterable[tuple[Any, Any, Any]]) -> list[str]:
    """Teks konteks yang menyertakan label manusiawi di samping IRI."""
    baris: list[str] = []
    for s, p, o in triple:
        baris.append(_n3(store, (s, p, o)))
        if isinstance(o, URIRef):
            label = store.nama(o)
            if label and not label.endswith(str(o).rsplit("/", 1)[-1]):
                baris.append(f'  # {o} = "{label}"')
    return baris
