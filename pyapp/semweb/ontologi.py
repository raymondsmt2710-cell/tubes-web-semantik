"""Pemeriksa kepatuhan ontologi — pengganti pemeriksaan manual di Protégé.

Materi P5 dan P12 menekankan bahwa ontologi yang salah tidak menimbulkan pesan
galat: ia hanya membuat kesimpulan yang keliru. Karena itu pemeriksaan ini
dijalankan sebagai skrip yang bisa diulang, bukan diperiksa dengan mata.

Lima aturan yang diperiksa (daftar tugas A2):

1. ``domain-range``        — setiap properti objek punya ``rdfs:domain`` dan
                             ``rdfs:range``, kecuali yang punya ``owl:inverseOf``.
2. ``makna-ganda``         — tidak ada properti yang sekaligus properti objek
                             dan properti data, dan properti objek tidak dipakai
                             dengan literal.
3. ``kelas-tak-deklarasi`` — setiap kelas yang dipakai data dideklarasikan
                             di ontologi. Disertai ``properti-tak-deklarasi``
                             untuk predikat, karena lubang yang sama bisa
                             terjadi pada properti.
4. ``disjoint``            — tidak ada individu yang menempati dua kelas
                             ``owl:disjointWith``.
5. ``subkelas-kosong``     — setiap subkelas ``sdp:Museum`` punya individu.

Aturan 1 sengaja mengecualikan properti ber-``owl:inverseOf``. README proyek
menyatakan properti semacam itu **tidak** menyimpan domain/range eksplisit
supaya graf tetap konsisten di bawah OWL 2 RL; pasangannya yang menyimpan, dan
reasoner menurunkan sisanya. Pemeriksa yang menuntutnya akan menyalahkan
keputusan desain yang sudah dipegang proyek.
"""

from __future__ import annotations

from dataclasses import dataclass

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from .namespace import SDP

__all__ = ["Temuan", "periksa_ontologi"]


@dataclass(frozen=True)
class Temuan:
    """Satu pelanggaran aturan, cukup rinci untuk ditindaklanjuti."""

    aturan: str
    pesan: str

    def __str__(self) -> str:
        return f"[{self.aturan}] {self.pesan}"


def _lokal(iri: URIRef) -> str:
    """Nama pendek sebuah IRI untuk pesan yang mudah dibaca."""
    teks = str(iri)
    for pemisah in ("#", "/"):
        if pemisah in teks:
            teks = teks.rsplit(pemisah, 1)[-1]
    return teks


def _subjek_bertipe(graf: Graph, kelas: URIRef) -> set[URIRef]:
    """Individu bertipe ``kelas``, langsung maupun lewat subkelasnya.

    Data museum menulis tipe spesifik (``StateMuseum``), bukan ``Museum``;
    tipe induk baru muncul setelah penalaran. Karena itu subkelas ikut
    ditelusuri supaya pemeriksaan tidak buta terhadap data yang sebenarnya.
    """
    kandidat = {kelas}
    for sub in graf.subjects(RDFS.subClassOf, kelas):
        if isinstance(sub, URIRef):
            kandidat.add(sub)

    hasil: set[URIRef] = set()
    for k in kandidat:
        for subjek in graf.subjects(RDF.type, k):
            if isinstance(subjek, URIRef):
                hasil.add(subjek)
    return hasil


def _properti(graf: Graph, jenis: URIRef) -> set[URIRef]:
    return {p for p in graf.subjects(RDF.type, jenis) if isinstance(p, URIRef)}


def _cek_domain_range(onto: Graph) -> list[Temuan]:
    """Aturan 1: properti objek punya domain dan range, kecuali ber-inverse."""
    temuan: list[Temuan] = []
    for prop in sorted(_properti(onto, OWL.ObjectProperty), key=_lokal):
        if (prop, OWL.inverseOf, None) in onto:
            continue
        hilang = [
            nama
            for nama, predikat in (
                ("domain", RDFS.domain),
                ("range", RDFS.range),
            )
            if (prop, predikat, None) not in onto
        ]
        if hilang:
            temuan.append(
                Temuan(
                    "domain-range",
                    f"sdp:{_lokal(prop)} tidak punya {' dan '.join(hilang)}",
                )
            )
    return temuan


def _cek_makna_ganda(onto: Graph, data: Graph) -> list[Temuan]:
    """Aturan 2: satu properti, satu arti."""
    temuan: list[Temuan] = []
    objek = _properti(onto, OWL.ObjectProperty)
    data_prop = _properti(onto, OWL.DatatypeProperty)

    for prop in sorted(objek & data_prop, key=_lokal):
        temuan.append(
            Temuan(
                "makna-ganda",
                f"sdp:{_lokal(prop)} dideklarasikan sebagai properti objek "
                "sekaligus properti data",
            )
        )

    for prop in sorted(objek, key=_lokal):
        for _, _, objek_triple in data.triples((None, prop, None)):
            if isinstance(objek_triple, Literal):
                temuan.append(
                    Temuan(
                        "makna-ganda",
                        f"sdp:{_lokal(prop)} adalah properti objek tetapi "
                        f'dipakai dengan literal "{objek_triple}"',
                    )
                )
                break
    return temuan


def _cek_deklarasi(onto: Graph, data: Graph) -> list[Temuan]:
    """Aturan 3: semua kelas dan properti yang dipakai data ada di ontologi."""
    temuan: list[Temuan] = []

    kelas_onto = {
        k
        for k in onto.subjects(RDF.type, OWL.Class)
        if isinstance(k, URIRef) and str(k).startswith(str(SDP))
    }
    kelas_data = {
        o
        for o in data.objects(None, RDF.type)
        if isinstance(o, URIRef) and str(o).startswith(str(SDP))
    }
    for kelas in sorted(kelas_data - kelas_onto, key=_lokal):
        jumlah = sum(1 for _ in data.subjects(RDF.type, kelas))
        temuan.append(
            Temuan(
                "kelas-tak-deklarasi",
                f"sdp:{_lokal(kelas)} dipakai {jumlah} individu di data "
                "tetapi tidak dideklarasikan sebagai owl:Class",
            )
        )

    prop_onto = _properti(onto, OWL.ObjectProperty) | _properti(
        onto, OWL.DatatypeProperty
    )
    prop_data = {
        p
        for p in data.predicates()
        if isinstance(p, URIRef) and str(p).startswith(str(SDP))
    }
    for prop in sorted(prop_data - prop_onto, key=_lokal):
        jumlah = sum(1 for _ in data.triples((None, prop, None)))
        temuan.append(
            Temuan(
                "properti-tak-deklarasi",
                f"sdp:{_lokal(prop)} dipakai {jumlah} triple di data tetapi "
                "tidak dideklarasikan sebagai properti",
            )
        )
    return temuan


def _cek_disjoint(onto: Graph, data: Graph) -> list[Temuan]:
    """Aturan 4: tidak ada individu yang menempati dua kelas disjoint."""
    temuan: list[Temuan] = []
    pasangan = {
        (a, b)
        for a, b in onto.subject_objects(OWL.disjointWith)
        if isinstance(a, URIRef) and isinstance(b, URIRef)
    }
    # disjointWith simetris; periksa kedua arah.
    pasangan |= {(b, a) for a, b in pasangan}

    for kiri, kanan in sorted(pasangan, key=lambda p: (_lokal(p[0]), _lokal(p[1]))):
        anggota_kiri = _subjek_bertipe(data, kiri)
        anggota_kanan = _subjek_bertipe(data, kanan)
        for subjek in sorted(anggota_kiri & anggota_kanan, key=_lokal):
            temuan.append(
                Temuan(
                    "disjoint",
                    f"{_lokal(subjek)} bertipe sdp:{_lokal(kiri)} sekaligus "
                    f"sdp:{_lokal(kanan)}, padahal keduanya owl:disjointWith",
                )
            )
    return temuan


def _cek_subkelas_kosong(onto: Graph, data: Graph) -> list[Temuan]:
    """Aturan 5: setiap subkelas sdp:Museum punya individu."""
    temuan: list[Temuan] = []
    for sub in sorted(
        {s for s in onto.subjects(RDFS.subClassOf, SDP.Museum) if isinstance(s, URIRef)},
        key=_lokal,
    ):
        if not _subjek_bertipe(data, sub):
            temuan.append(
                Temuan(
                    "subkelas-kosong",
                    f"sdp:{_lokal(sub)} adalah subkelas sdp:Museum tetapi "
                    "tidak punya satu pun individu di data",
                )
            )
    return temuan


def periksa_ontologi(onto: Graph, data: Graph) -> list[Temuan]:
    """Jalankan kelima aturan dan kembalikan seluruh temuan.

    Daftar kosong berarti ontologi patuh. Temuan dikembalikan semua sekaligus
    — bukan berhenti di yang pertama — supaya satu kali jalan memberi daftar
    pekerjaan yang lengkap.
    """
    return [
        *_cek_domain_range(onto),
        *_cek_makna_ganda(onto, data),
        *_cek_deklarasi(onto, data),
        *_cek_disjoint(onto, data),
        *_cek_subkelas_kosong(onto, data),
    ]
