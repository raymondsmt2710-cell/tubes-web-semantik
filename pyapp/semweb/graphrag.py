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


# Kata yang menyebut jenis entitas, bukan nama diri. Kata-kata ini dibuang
# sebelum mencocokkan label sebagian, karena "Museum Aceh" tidak boleh dicocokkan
# sebagai nama museum yang memuat kata "museum".
_KATA_UMUM = {
    "museum",
    "museums",
    "kota",
    "kabupaten",
    "provinsi",
    "propinsi",
    "daerah",
    "tema",
    "era",
    "pameran",
    "koleksi",
    "foto",
    "galeri",
    "sejarah",
    "di",
    "ke",
    "dari",
    "yang",
    "apa",
    "saja",
    "ada",
    "berapa",
    "jumlah",
    "kapan",
    "bagaimana",
    "dan",
    "atau",
    "dengan",
    "untuk",
    "isi",
    "punya",
    "memiliki",
}

# Kata yang menandakan pertanyaan menyebut **nama diri**, bukan wilayah.
# Jalur pencocokan sebagian hanya masuk akal bila salah satunya muncul: tanpa
# itu, "museum apa saja di Aceh" akan salah dianggap menyebut museum tertentu.
_KATA_NAMA = {"museum", "museums"}

# Kata tanya menandakan pertanyaan tentang kategori, bukan penamaan entitas.
# Bila salah satunya muncul, jalur pencocokan sebagian tidak dijalankan.
_KATA_TANYA = {
    "apa",
    "saja",
    "berapa",
    "mana",
    "kapan",
    "bagaimana",
    "siapa",
    "jumlah",
}

# Kata wilayah: pertanyaan yang menyebutnya sedang menyaring per wilayah, bukan
# menamai museum. "museum di Aceh" harus menghasilkan jangkar provinsi, bukan
# dua museum yang kebetulan berbagi kata "aceh".
_KATA_WILAYAH = {"kota", "kabupaten", "provinsi", "propinsi", "daerah", "wilayah"}

# Preposisi lokasi menandakan penyaringan wilayah, bukan penamaan entitas.
# "museum di Aceh" memakai "di"; "Museum Aceh" tidak.
_KATA_LOKASI = {"di", "dari", "ke", "pada", "dalam"}


def _kata_bermakna(teks: str) -> set[str]:
    """Kata isi pada pertanyaan, tanpa kata umum dan tanpa angka/tanda baca."""
    hasil: set[str] = set()
    for bagian in re.split(r"[^\w]+", teks.lower()):
        if len(bagian) < 3:
            continue
        if bagian in _KATA_UMUM:
            continue
        if bagian.isdigit():
            continue
        hasil.add(bagian)
    return hasil


def _kata_bermakna_awal(teks: str) -> set[str]:
    """Semua kata pada teks, termasuk kata pendek dan kata umum.

    Dipakai hanya untuk memeriksa niat pertanyaan: apakah ia bertanya tentang
    kategori, menyaring wilayah, atau menamai entitas. Kata pendek tetap
    dipertahankan di sini karena "di" dan "ke" justru penanda lokasi.
    """
    hasil: set[str] = set()
    for bagian in re.split(r"[^\w]+", teks.lower()):
        if not bagian:
            continue
        hasil.add(bagian)
    return hasil


def _skor_sebagian(teks: str, label: str) -> float:
    """Seberapa cocok label dengan pertanyaan yang menyebut namanya sebagian.

    Dua sisi dihitung, karena satu sisi saja membuat dua museum berbeda mendapat
    skor sama:

    - **Cakupan pertanyaan**: berapa bagian kata isi pertanyaan yang ada di label.
    - **Kekhususan label**: berapa bagian kata isi label yang disebut pertanyaan.

    Contoh: pertanyaan "museum aceh" terhadap dua label.

    - "Museum Negeri Aceh": cakupan 1/1, kekhususan 1/2 -> 0.5
    - "Museum Tsunami Aceh": cakupan 1/1, kekhususan 1/2 -> 0.5

    Keduanya seri, dan itu memang benar: "Museum Aceh" **ambigu** antara dua
    museum. Jangkar mengembalikan keduanya, dan lapisan jawaban yang menyebut
    ambiguitas. Yang tidak boleh terjadi adalah memilih salah satu tanpa dasar.

    Bila hanya satu museum yang cocok, skornya tetap dipakai apa adanya.
    """
    kata_tanya = _kata_bermakna(teks)
    if not kata_tanya:
        return 0.0

    kata_label = _kata_bermakna(label)
    if not kata_label:
        return 0.0

    cocok = kata_tanya & kata_label
    if not cocok:
        return 0.0

    cakupan = len(cocok) / len(kata_tanya)
    kekhususan = len(cocok) / len(kata_label)

    return cakupan * 0.5 + kekhususan * 0.5


def jangkar(store: MuseumStore, pertanyaan: str, maks: int = 3) -> list[Jangkar]:
    """Temukan entitas jangkar yang disebut pada pertanyaan.

    Tiga hal dijaga supaya jangkar tidak meleset:

    - **Label terpanjang menang.** "Museum Negeri Aceh" harus mengalahkan
      "Aceh" bila keduanya muncul, karena label panjang lebih spesifik.
    - **Batas kata.** Pencocokan memakai batas kata, bukan ``in`` biasa.
    - **Nama sebagian tetap dikenali.** Pertanyaan "Museum Aceh" tidak memuat
      label utuh mana pun, tetapi jelas menunjuk museum. Bila pencocokan utuh
      tidak menghasilkan **satu pun museum**, jalur kedua mencocokkan kata isi
      dan memilih museum dengan skor tertinggi.
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

    # Subkelas museum (`StateMuseum`/`SiteMuseum`/`PrivateMuseum`) ditulis di
    # data sebagai tipe spesifik; `sdp:Museum` baru diturunkan reasoner. Karena
    # itu pencarian jangkar harus ikut menelusuri subkelas, kalau tidak museum
    # tidak pernah ditemukan dan jangkar jatuh ke provinsi/kota.
    jenis_museum = {SDP.Museum} | {
        s
        for s in store.asserted.subjects(RDFS.subClassOf, SDP.Museum)
        if isinstance(s, URIRef)
    }

    kandidat_museum: list[tuple[URIRef, str]] = []
    for kelas_nyata in jenis_museum:
        for node in store.asserted.subjects(RDF.type, kelas_nyata):
            if not isinstance(node, URIRef):
                continue
            label = store.nama(node)
            if label:
                kandidat_museum.append((node, label))

    temuan: list[tuple[int, int, Jangkar]] = []
    sudah: set[str] = set()

    for kelas, (urutan, jenis) in prioritas_jenis.items():
        if kelas == SDP.Museum:
            pasangan = kandidat_museum
        else:
            pasangan = [
                (node, store.nama(node))
                for node in store.asserted.subjects(RDF.type, kelas)
                if isinstance(node, URIRef)
            ]

        for node, label in pasangan:
            if not label or not _memuat(teks, label):
                continue
            if str(node) in sudah:
                continue
            sudah.add(str(node))
            temuan.append((-len(label), urutan, Jangkar(node, label, jenis)))

    ada_museum = any(j.jenis == "museum" for _, _, j in temuan)

    kata_awal = _kata_bermakna_awal(teks)
    bertanya_kategori = bool(kata_awal & _KATA_TANYA)
    menyaring_wilayah = bool(kata_awal & (_KATA_WILAYAH | _KATA_LOKASI))

    if not ada_museum and not bertanya_kategori and not menyaring_wilayah:
        # Jalur kedua: nama disebut sebagian. Hanya dijalankan bila pencocokan
        # utuh tidak menemukan museum sama sekali **dan** pertanyaan tidak
        # berbentuk pertanyaan kategori ("apa saja", "berapa", "mana").
        # Tanpa syarat kedua, "museum apa saja di Aceh" akan salah dianggap
        # menamai museum tertentu.
        sebagian: list[tuple[float, int, Jangkar]] = []
        for node, label in kandidat_museum:
            if str(node) in sudah:
                continue
            skor = _skor_sebagian(teks, label)
            if skor <= 0.0:
                continue
            sebagian.append((skor, -len(label), Jangkar(node, label, "museum")))

        if sebagian:
            sebagian.sort(key=lambda t: (t[0], t[1]), reverse=True)
            teratas = sebagian[0][0]
            for skor, _, j in sebagian:
                if skor < teratas:
                    continue
                if str(j.iri) in sudah:
                    continue
                sudah.add(str(j.iri))
                temuan.append((-len(j.label), 0, j))

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
