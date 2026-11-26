"""Penalaran: apa yang ditulis, apa yang diturunkan, dan mengapa.

Materi P12 menegaskan urutannya: reasoner tidak mengubah fakta yang ditulis. Ia
menambahkan fakta turunan, lalu query bekerja pada closure. Modul ini membuat
perbedaan itu bisa dilihat pengguna — bukan hanya dijelaskan.
"""

from __future__ import annotations

from typing import Any

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from .namespace import RES, SDP
from .store import MuseumStore

# Predikat yang isinya aksioma vocabulary, bukan pengetahuan tentang data museum.
# `owl:sameAs` ikut dibuang seluruhnya: reasoner menurunkan `x owl:sameAs x` untuk
# setiap individu (2.316 triple di data asli). Dulu penyaringnya bersyarat
# `s == o`, sehingga hanya refleksivitas yang tertahan dan `sameAs` antar dua IRI
# berbeda tetap lolos ke daftar fakta — padahal itu artefak mesin, bukan temuan.
_AKSIOMA_PREDIKAT = frozenset(
    {
        OWL.sameAs,
        RDFS.domain,
        RDFS.range,
        RDFS.subClassOf,
        RDFS.subPropertyOf,
        OWL.equivalentClass,
        OWL.equivalentProperty,
    }
)

# Objek yang selalu benar untuk hampir semua node, jadi menyebutnya tidak
# menambah informasi apa pun bagi pembaca.
_OBJEK_TRIVIAL = frozenset({OWL.Thing, OWL.Nothing, RDFS.Resource})


def perbandingan(store: MuseumStore) -> dict[str, int]:
    """Empat angka yang dipakai halaman metode: asserted, dua closure, turunan."""
    return {
        "asserted": len(store.asserted),
        "closure_owlrl": len(store.closure),
        "closure_rdfs": len(store.rdfs),
        "inferred": len(store.closure) - len(store.asserted),
    }


def _n3(store: MuseumStore, node) -> str:
    """Tulis node dalam notasi berprefiks agar mudah dibaca manusia."""
    if isinstance(node, Literal):
        return f'"{node}"'
    try:
        return store.asserted.namespace_manager.normalizeUri(node)
    except Exception:
        return str(node)


def fakta_turunan(
    store: MuseumStore,
    subjek: URIRef | None = None,
    batas: int = 50,
) -> list[dict[str, Any]]:
    """Fakta yang ada di closure tetapi tidak pernah ditulis di data.

    Yang ditampilkan hanya fakta tentang entitas museum (museum, pameran, foto,
    kota, dan provinsi). Selebihnya adalah aksioma bawaan vocabulary OWL/XSD
    yang benar tetapi tidak menjelaskan apa pun tentang data kita — misalnya
    `owl:Nothing rdfs:subClassOf sdp:Museum` yang selalu benar secara logika.

    Hasil diurutkan menurut `(subjek, predikat, objek)` **sebelum** dipotong
    `batas`, supaya halaman yang menampilkan sebagian fakta tidak berubah-ubah
    isinya setiap kali dimuat (urutan iterasi graf tidak dijamin).
    """
    asserted = set(store.asserted)
    terlihat: set[tuple[str, str, str]] = set()
    hasil: list[dict[str, Any]] = []

    pola = (subjek, None, None) if subjek is not None else (None, None, None)
    for s, p, o in store.closure.triples(pola):
        if isinstance(s, BNode) or isinstance(o, BNode):
            continue
        if (s, p, o) in asserted:
            continue

        # Hanya entitas data kita sendiri; aksioma vocabulary dilewati.
        if not str(s).startswith(str(RES)):
            continue
        if p in _AKSIOMA_PREDIKAT:
            continue
        if isinstance(o, URIRef) and o in _OBJEK_TRIVIAL:
            continue

        kunci = (str(s), str(p), str(o))
        if kunci in terlihat:
            continue
        terlihat.add(kunci)

        hasil.append(
            {
                "subjek": kunci[0],
                "predikat": kunci[1],
                "objek": kunci[2],
                "subjek_n3": _n3(store, s),
                "predikat_n3": _n3(store, p),
                "objek_n3": _n3(store, o),
                # Task 5 akan menggantinya dengan nama aturan sebenarnya;
                # untuk sekarang nilai ini sah dan menjaga bentuk keluaran.
                "aturan": ["tidak teridentifikasi"],
            }
        )

    # Urutkan penuh dulu, baru potong: memotong sambil mengiterasi graf membuat
    # isi halaman bergantung pada urutan iterasi yang tidak dijamin stabil.
    hasil.sort(key=lambda f: (f["subjek"], f["predikat"], f["objek"]))
    return hasil[:batas]


def jelaskan_tipe(store: MuseumStore, slug: str) -> list[str]:
    """Susun rantai penalaran tipe museum dalam kalimat Bahasa Indonesia.

    Rantai ini memperlihatkan aturan `rdfs:subClassOf` bekerja: tipe yang ditulis
    di data, kelas atasnya, lalu kesimpulan yang tidak pernah ditulis.
    """
    museum = URIRef(f"{RES}museum/{slug}")
    if (museum, None, None) not in store.asserted:
        return [f"Museum dengan slug '{slug}' tidak ada di graf."]

    nama = store.nama(museum)
    kalimat: list[str] = []

    tipe_tertulis = [
        t
        for t in store.asserted.objects(museum, RDF.type)
        if isinstance(t, URIRef) and t != OWL.Thing
    ]
    for tipe in tipe_tertulis:
        kalimat.append(f"{nama} bertipe {_n3(store, tipe)} (ditulis di data).")

    # Telusuri rantai subClassOf hingga habis.
    for tipe in tipe_tertulis:
        sekarang = tipe
        dikunjungi: set[URIRef] = set()
        while True:
            induk = store.asserted.value(sekarang, RDFS.subClassOf)
            if not isinstance(induk, URIRef) or induk in dikunjungi:
                break
            dikunjungi.add(induk)
            if induk == OWL.Thing:
                break
            kalimat.append(
                f"{_n3(store, sekarang)} rdfs:subClassOf {_n3(store, induk)} (ditulis di data)."
            )
            if (museum, RDF.type, induk) in store.closure and (
                museum,
                RDF.type,
                induk,
            ) not in store.asserted:
                kalimat.append(
                    f"Maka {nama} juga bertipe {_n3(store, induk)} "
                    "(diturunkan reasoner, tidak pernah ditulis)."
                )
            sekarang = induk

    if len(kalimat) == len([k for k in kalimat if "bertipe" in k]):
        kalimat.append(
            "Tidak ada kelas atas tambahan, sehingga penalaran tidak menambah tipe baru."
        )

    return kalimat


def cek_konsistensi(store: MuseumStore) -> list[str]:
    """Laporkan individu yang menempati dua kelas `owl:disjointWith`.

    OWL tidak "menolak" data seperti constraint basis data — ia membuat model
    menjadi tidak konsisten. Pesan ini menyebut pasangan kelasnya supaya
    pemodelan yang keliru bisa diperbaiki di sumbernya.

    Pemeriksaan dilakukan pada **closure**, bukan hanya graf asserted: kelas
    disjoint sering baru terpenuhi lewat `rdfs:subClassOf` atau `rdfs:domain`,
    dan justru pelanggaran hasil inferensi itulah yang paling perlu dilihat —
    tidak ada di data mentah, jadi sulit ditemukan dengan mata.
    """
    pasangan: list[tuple[URIRef, URIRef]] = []
    for kiri, _, kanan in store.asserted.triples((None, OWL.disjointWith, None)):
        if isinstance(kiri, URIRef) and isinstance(kanan, URIRef):
            pasangan.append((kiri, kanan))
            pasangan.append((kanan, kiri))

    if not pasangan:
        return []

    pesan: list[str] = []
    terlihat: set[str] = set()

    # Telusuri tipe pada closure: gabungan tipe asserted + turunan.
    for node in set(store.closure.subjects(RDF.type, None)):
        if not isinstance(node, URIRef):
            continue
        tipe = {
            t for t in store.closure.objects(node, RDF.type) if isinstance(t, URIRef)
        }
        for kiri, kanan in pasangan:
            if kiri in tipe and kanan in tipe:
                kunci = f"{node}|{kiri}|{kanan}"
                if kunci in terlihat:
                    continue
                terlihat.add(kunci)
                asal = "akibat inferensi" if (
                    kanan not in set(store.asserted.objects(node, RDF.type))
                ) else ""
                akhiran = f" ({asal})" if asal else ""
                pesan.append(
                    f"{store.nama(node)} bertipe {_n3(store, kiri)} sekaligus "
                    f"{_n3(store, kanan)}, padahal keduanya owl:disjointWith{akhiran}."
                )
    return pesan
