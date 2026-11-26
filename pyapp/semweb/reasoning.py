"""Penalaran: apa yang ditulis, apa yang diturunkan, dan mengapa.

Materi P12 menegaskan urutannya: reasoner tidak mengubah fakta yang ditulis. Ia
menambahkan fakta turunan, lalu query bekerja pada closure. Modul ini membuat
perbedaan itu bisa dilihat pengguna — bukan hanya dijelaskan.
"""

from __future__ import annotations

from collections import deque
from typing import Any, NamedTuple

from rdflib import BNode, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from .namespace import RES
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
    """Tulis node dalam notasi berprefiks agar mudah dibaca manusia.

    `normalizeUri` tidak bisa dipakai apa adanya: `rdflib` hanya mau menyingkat
    IRI bila sisa setelah prefiks adalah nama lokal yang sah (tanpa `/`). IRI
    seperti `res:museum/museum-adityawarman` punya sisa `museum/museum-...`,
    sehingga rdflib menyerah dan mengembalikan IRI penuh — persis yang membuat
    justifikasi di `/metode` sulit dibaca. Karena itu `res:` dipotong manual.
    """
    if isinstance(node, Literal):
        return f'"{node}"'
    if isinstance(node, URIRef):
        teks = str(node)
        if teks.startswith(str(RES)):
            return f"res:{teks[len(str(RES)):]}"
    try:
        return store.premis.namespace_manager.normalizeUri(node)
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

    Hasil disimpan di cache milik store, berkunci `(subjek, batas)`: menyusuri
    closure dan mengatribusikan aturan tidak murah, sedangkan halaman memanggil
    fungsi ini pada setiap render dengan argumen yang sama. Cache menempel pada
    instance store — bukan kamus global berkunci `id(store)` — karena `id()`
    didaur ulang setelah garbage collection dan suite test membuat puluhan
    store; kunci seperti itu bisa mengembalikan fakta graf lain.
    """
    cache = getattr(store, "_cache_fakta_turunan", None)
    if cache is None:
        cache = {}
        store._cache_fakta_turunan = cache

    kunci = (subjek, batas)
    tersimpan = cache.get(kunci)
    if tersimpan is not None:
        return _salinan(tersimpan)

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

        kunci_fakta = (str(s), str(p), str(o))
        if kunci_fakta in terlihat:
            continue
        terlihat.add(kunci_fakta)

        hasil.append(
            {
                "subjek": kunci_fakta[0],
                "predikat": kunci_fakta[1],
                "objek": kunci_fakta[2],
                "subjek_n3": _n3(store, s),
                "predikat_n3": _n3(store, p),
                "objek_n3": _n3(store, o),
            }
        )

    # Urutkan penuh dulu, baru potong: memotong sambil mengiterasi graf membuat
    # isi halaman bergantung pada urutan iterasi yang tidak dijamin stabil.
    hasil.sort(key=lambda f: (f["subjek"], f["predikat"], f["objek"]))
    hasil = hasil[:batas]

    # Atribusi aturan dikerjakan **setelah** pemotongan: `aturan_fakta` menyusuri
    # graf premis per fakta, dan pemanggil yang hanya minta 20 baris tidak perlu
    # justifikasi seluruh ratusan fakta. Nilainya daftar nama aturan, bukan objek
    # justifikasi penuh — halaman hanya menyebut aturan mana yang bekerja.
    for fakta in hasil:
        fakta["aturan"] = [a["aturan"] for a in aturan_fakta(store, fakta)]

    cache[kunci] = hasil
    return _salinan(hasil)


def _salinan(fakta: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Salinan yang boleh dipegang pemanggil tanpa merusak cache.

    `aturan` ikut disalin karena ia satu-satunya nilai bersarang: salinan dangkal
    biasa masih membiarkan pemanggil mengubah isi cache lewat daftar itu.
    """
    return [dict(f, aturan=list(f["aturan"])) for f in fakta]


_URUTAN_ATURAN = ("prp-inv", "prp-symp", "rdfs9", "rdfs11", "rdfs2", "rdfs3")


def _kalimat(store: MuseumStore, s, p, o) -> str:
    """Satu triple premis sebagai kalimat yang bisa dibaca manusia."""
    return f"{_n3(store, s)} {_n3(store, p)} {_n3(store, o)}"


class _Aksioma(NamedTuple):
    """Indeks aksioma skema, dikunci menurut peran yang dicari.

    Setiap peta dikunci objek yang muncul di **ruas kanan** aksioma (kelas untuk
    `domain`/`range`, properti tujuan untuk `inverseOf`, subkelas untuk
    `subClassOf`), karena justifikasi selalu bermula dari fakta lalu mencari
    aksioma yang cocok dengannya — bukan sebaliknya.
    """

    inverse: dict[URIRef, set[URIRef]]
    domain: dict[URIRef, set[URIRef]]
    rentang: dict[URIRef, set[URIRef]]
    subkelas: dict[URIRef, set[URIRef]]


def _peta_aksioma(premis) -> _Aksioma:
    """Bangun indeks aksioma sekali, lalu pakai untuk semua aturan."""
    inverse: dict[URIRef, set[URIRef]] = {}
    for a, _, b in premis.triples((None, OWL.inverseOf, None)):
        # Dua arah: `owl:inverseOf` simetris menurut OWL, dan ontologi hanya
        # menulis satu arah untuk sebagian pasangan.
        inverse.setdefault(a, set()).add(b)
        inverse.setdefault(b, set()).add(a)

    domain: dict[URIRef, set[URIRef]] = {}
    for p, _, c in premis.triples((None, RDFS.domain, None)):
        domain.setdefault(c, set()).add(p)

    rentang: dict[URIRef, set[URIRef]] = {}
    for p, _, c in premis.triples((None, RDFS.range, None)):
        rentang.setdefault(c, set()).add(p)

    subkelas: dict[URIRef, set[URIRef]] = {}
    for a, _, b in premis.triples((None, RDFS.subClassOf, None)):
        subkelas.setdefault(a, set()).add(b)

    return _Aksioma(inverse, domain, rentang, subkelas)


def _peta_aksioma_tercache(store: MuseumStore) -> _Aksioma:
    """Indeks aksioma dibangun sekali per store, bukan sekali per fakta.

    `fakta_turunan` memanggil `aturan_fakta` untuk setiap fakta yang ditampilkan,
    dan membangun ulang indeks di tiap panggilan berarti menggambar ulang graf
    premis 300-an kali. Indeks ini hanya bergantung pada `store.premis`, yang
    tidak berubah setelah store dibuat, jadi aman disimpan pada instance.
    """
    peta = getattr(store, "_cache_peta_aksioma", None)
    if peta is None:
        peta = _peta_aksioma(store.premis)
        store._cache_peta_aksioma = peta
    return peta


def _jejak_subkelas(
    subkelas: dict[URIRef, set[URIRef]], awal: URIRef, target: URIRef
) -> list[URIRef] | None:
    """Rantai `subClassOf` terpendek dari `awal` ke `target`, atau None.

    Rantai dikembalikan utuh (termasuk kedua ujungnya) karena pembaca perlu
    melihat tiap langkah yang dipakai — bukan hanya kesimpulan akhirnya.
    Pencarian melebar dan berhenti di jalur terpendek supaya `rdfs9` (1 langkah)
    dan `rdfs11` (≥ 2 langkah) bisa dibedakan tanpa menebak. Induk diurutkan
    supaya bila ada beberapa jalur sama panjang, yang dilaporkan selalu sama
    di setiap proses (urutan himpunan tidak dijamin stabil).
    """
    antre: deque[list[URIRef]] = deque([[awal]])
    dilihat: set[URIRef] = {awal}
    while antre:
        jalur = antre.popleft()
        for induk in sorted(subkelas.get(jalur[-1], ()), key=str):
            if induk == target:
                return jalur + [induk]
            if induk not in dilihat:
                dilihat.add(induk)
                antre.append(jalur + [induk])
    return None


def aturan_fakta(store: MuseumStore, fakta: dict[str, Any]) -> list[dict[str, Any]]:
    """Cari aturan penalaran yang menghasilkan satu fakta turunan.

    Setiap aturan yang **premisnya benar-benar ada di `store.premis`** dilaporkan,
    bukan hanya satu yang dipilih diam-diam: sebuah fakta bisa sah diturunkan
    lewat dua jalan (misalnya tipe dari `rdfs:domain` sekaligus dari
    `rdfs:subClassOf`), dan menyembunyikan salah satunya membuat justifikasi di
    `/metode` tidak bisa diperiksa ulang oleh pembaca.

    `owl:inverseOf` diperlakukan **simetris** karena ontologi hanya menulis satu
    arah untuk sebagian pasangan (`sdp:hasExhibit owl:inverseOf
    sdp:exhibitOfMuseum` ada, arah sebaliknya tidak). Semantik OWL memang
    simetris, jadi peta dibangun dua arah — tanpa itu seluruh fakta `prp-inv`
    akan tampil sebagai `tidak teridentifikasi`.

    Bila tidak ada aturan yang cocok, kembalikan `tidak teridentifikasi` dengan
    `premis` kosong: itu alarm jujur bahwa reasoner menghasilkan sesuatu di luar
    aturan yang kita kenali, bukan alasan untuk menebak.
    """
    subjek = URIRef(fakta["subjek"])
    predikat = URIRef(fakta["predikat"])
    objek = URIRef(fakta["objek"])
    premis = store.premis
    peta = _peta_aksioma_tercache(store)

    hasil: dict[str, list[str]] = {}

    # prp-inv: (P inverseOf Q) + (objek Q subjek) => (subjek P objek).
    # Kalimat aksiomanya menyebut arah yang **benar-benar tertulis** di premis:
    # ontologi hanya menulis sebagian pasangan satu arah, jadi menulis arah
    # sebaliknya berarti mengarang premis yang tidak ada di graf.
    for q in sorted(peta.inverse.get(predikat, ()), key=str):
        if (objek, q, subjek) not in premis:
            continue
        aksioma = (
            (predikat, OWL.inverseOf, q)
            if (predikat, OWL.inverseOf, q) in premis
            else (q, OWL.inverseOf, predikat)
        )
        hasil.setdefault("prp-inv", []).extend(
            [_kalimat(store, *aksioma), _kalimat(store, objek, q, subjek)]
        )

    # prp-symp: properti simetris + pasangan terbalik sudah ada.
    if (predikat, RDF.type, OWL.SymmetricProperty) in premis and (
        objek,
        predikat,
        subjek,
    ) in premis:
        hasil.setdefault("prp-symp", []).extend(
            [
                _kalimat(store, predikat, RDF.type, OWL.SymmetricProperty),
                _kalimat(store, objek, predikat, subjek),
            ]
        )

    if predikat == RDF.type:
        # rdfs2: (P domain C) + subjek memakai P => subjek bertipe C.
        # Setiap aksioma domain yang premisnya terpenuhi dilaporkan; pada data ini
        # museum memang memakai belasan properti berdomain sdp:Museum, dan
        # menyembunyikan sebagian akan membuat justifikasinya tidak lengkap.
        #
        # Satu saksi per properti, bukan per nilai: museum dengan tiga tema akan
        # mengulang kalimat aksioma yang sama tiga kali tanpa menambah informasi.
        for p in sorted(peta.domain.get(objek, ()), key=str):
            nilai = next(iter(sorted(premis.objects(subjek, p), key=str)), None)
            if nilai is None:
                continue
            hasil.setdefault("rdfs2", []).extend(
                [_kalimat(store, p, RDFS.domain, objek), _kalimat(store, subjek, p, nilai)]
            )

        # rdfs3: (P range C) + ada x P objek => x bertipe C, sehingga objek
        # (subjek fakta ini) bertipe C bila ia dipakai sebagai objek P.
        for p in sorted(peta.rentang.get(objek, ()), key=str):
            for sumber in sorted(premis.subjects(p, subjek), key=str):
                hasil.setdefault("rdfs3", []).extend(
                    [_kalimat(store, p, RDFS.range, objek), _kalimat(store, sumber, p, subjek)]
                )

        # rdfs9 (1 langkah) dan rdfs11 (>= 2 langkah) saling eksklusif: jarak
        # rantai yang menentukan namanya, bukan tebakan.
        for tipe in sorted(
            (t for t in premis.objects(subjek, RDF.type) if isinstance(t, URIRef)), key=str
        ):
            jalur = _jejak_subkelas(peta.subkelas, tipe, objek)
            if not jalur:
                continue
            nama = "rdfs9" if len(jalur) == 2 else "rdfs11"
            kalimat = [_kalimat(store, subjek, RDF.type, tipe)]
            kalimat.extend(
                _kalimat(store, kiri, RDFS.subClassOf, kanan)
                for kiri, kanan in zip(jalur, jalur[1:])
            )
            hasil.setdefault(nama, []).extend(kalimat)

    if not hasil:
        return [{"aturan": "tidak teridentifikasi", "premis": []}]

    return [
        {"aturan": nama, "premis": hasil[nama]} for nama in _URUTAN_ATURAN if nama in hasil
    ]


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
