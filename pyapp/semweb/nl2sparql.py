"""NL2SPARQL: pertanyaan bahasa Indonesia menjadi query SPARQL.

Materi P13 membagi alur menjadi **empat langkah**, dan modul ini mengikutinya:

1. **Skema** — hanya IRI yang benar-benar ada di graf yang boleh dipakai.
2. **Contoh** — beberapa pola pertanyaan/query dasar, bukan satu contoh saja.
3. **Validasi** — query di-*parse* sebelum dijalankan (lihat :func:`aman`).
4. **Verbalisasi** — jawaban disusun **dari data**, dan IRI sumber ditempel
   oleh kode, bukan oleh model.

Penerjemah di sini berbasis **aturan** (deterministik), dengan opsi model
bahasa lewat parameter ``penerjemah``. Hasilnya bisa diuji tanpa jaringan, dan
alasan setiap query dapat dijelaskan. Ketika model dipakai, query-nya tetap
melewati guard yang sama.

Yang **tidak** dilakukan modul ini: guard memeriksa bentuk dan kosakata query,
**bukan** hak akses pengguna. Otorisasi harus dilakukan di server.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

from rdflib import URIRef
from rdflib.paths import Path
from rdflib.plugins.sparql import prepareQuery

from .graphrag import ambil_konteks, jangkar as cari_jangkar
from .namespace import SDP
from .search import NAMA
from .sparql import PREFIX_MAP, PREFIXES, bersihkan_kata, label_slug, literal
from .store import MuseumStore

__all__ = [
    "ATURAN_VERBALISASI",
    "Hasil",
    "Skema",
    "aman",
    "intent",
    "jawab",
    "ke_sparql",
    "kosakata",
    "prompt",
    "skema_graf",
]

MAKS_LIMIT = 50

ATURAN_VERBALISASI = (
    "Jawab HANYA dari data di bawah. Jika data tidak cukup, katakan tidak cukup. "
    "Jangan menambah fakta dari ingatan Anda."
)


# --------------------------------------------------------------------- skema


@dataclass
class Skema:
    """Kosakata graf: kelas dan properti yang boleh muncul di query."""

    kelas: dict[str, str] = field(default_factory=dict)
    objek: dict[str, str] = field(default_factory=dict)
    data: dict[str, str] = field(default_factory=dict)

    def semua_iri(self) -> set[str]:
        return set(self.kelas) | set(self.objek) | set(self.data)

    def teks(self) -> str:
        """Ringkasan skema untuk prompt model (hanya bagian yang relevan)."""
        baris = ["# KELAS"]
        baris += [f"sdp:{n}" for n in sorted(self.kelas.values())]
        baris.append("# OBJECT PROPERTY")
        baris += [f"sdp:{n} ({d})" for n, d in sorted(self.objek.items())]
        baris.append("# DATA PROPERTY")
        baris += [f"sdp:{n}" for n in sorted(self.data.values())]
        return "\n".join(baris)


def skema_graf(store: MuseumStore) -> Skema:
    """Baca kelas dan properti dari graf asserted (P13 bagian 14)."""
    from rdflib.namespace import OWL, RDF, RDFS

    g = store.asserted
    skema = Skema()

    for kelas in g.subjects(RDF.type, OWL.Class):
        if isinstance(kelas, URIRef) and str(kelas).startswith(str(SDP)):
            skema.kelas[str(kelas)] = label_slug(kelas)
    for kelas in g.objects(None, RDF.type):
        if isinstance(kelas, URIRef) and str(kelas).startswith(str(SDP)):
            skema.kelas.setdefault(str(kelas), label_slug(kelas))

    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        if isinstance(prop, URIRef) and str(prop).startswith(str(SDP)):
            rng = g.value(prop, RDFS.range)
            skema.objek[str(prop)] = label_slug(rng) if rng is not None else "-"

    for _, p, o in g:
        if not isinstance(p, URIRef) or not str(p).startswith(str(SDP)):
            continue
        if isinstance(o, URIRef):
            skema.objek.setdefault(str(p), "-")
        else:
            skema.data.setdefault(str(p), label_slug(p))

    # Nama alternatif (rdfs:label) juga harus dikenal guard.
    skema.data.setdefault(str(RDFS.label), "label")
    skema.data.setdefault(str(SDP.name), "name")

    return skema


def kosakata(store: MuseumStore) -> set[str]:
    """Semua IRI yang boleh dipakai: isi graf ditambah kosakata standar."""
    BAKU = {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "http://www.w3.org/2000/01/rdf-schema#label",
        "http://www.w3.org/2000/01/rdf-schema#subClassOf",
    }
    isi = {str(x) for triple in store.asserted for x in triple if isinstance(x, URIRef)}
    return isi | BAKU | set(skema_graf(store).semua_iri())


# ---------------------------------------------------------------- intent


@dataclass
class Intent:
    """Hasil pembacaan pertanyaan: apa yang ditanya dan tentang apa."""

    jenis: str  # "daftar" | "hitung" | "atribut" | "tidak_dikenal"
    topik: str  # "museum" | "pameran" | "galeri" | "provinsi" | ...
    jangkar: str | None = None
    atribut: str | None = None
    kata: list[str] = field(default_factory=list)
    alasan: str = ""


_TOPIK: list[tuple[str, tuple[str, ...]]] = [
    ("pameran", ("pameran", "koleksi", "benda", "exhibit")),
    ("galeri", ("galeri", "foto", "gambar", "image")),
    ("provinsi", ("provinsi",)),
    ("kota", ("kota", "kabupaten")),
    ("tema", ("tema",)),
    ("era", ("era", "masa", "zaman")),
]

_HITUNG = ("berapa", "jumlah", "banyak", "hitung", "total")

# Kata yang menandakan pertanyaan di luar kemampuan graf. Graf menyimpan fakta
# museum (lokasi, tema, era, pameran, foto), bukan harga tiket atau jam buka —
# jadi menyebut kata-kata ini berarti pertanyaannya tidak bisa dijawab, walau
# nama museum atau provinsi ikut disebut.
_DI_LUAR_DOMAIN = (
    "harga",
    "tiket",
    "biaya",
    "tarif",
    "bayar",
    "jam buka",
    "jam operasional",
    "jadwal",
    "parkir",
    "toilet",
    "makanan",
    "penginapan",
    "hotel",
    "transportasi",
    "cuaca",
    "presiden",
    "mobil",
)


def _bersih(teks: str) -> str:
    """Rapikan pertanyaan: huruf kecil, spasi tunggal, tanpa tanda baca akhir."""
    rapi = re.sub(r"\s+", " ", (teks or "").strip().lower())
    return rapi.rstrip("?.!")


def _ada_kata(teks: str, kunci: str) -> bool:
    """Apakah ``kunci`` muncul sebagai kata utuh di ``teks``.

    Pencocokan memakai batas kata supaya "era" tidak cocok di dalam "berapa".
    """
    return re.search(r"(?<!\w)" + re.escape(kunci) + r"(?!\w)", teks) is not None


def intent(pertanyaan: str, store: MuseumStore | None = None) -> Intent:
    """Baca maksud pertanyaan bahasa Indonesia tanpa model bahasa.

    Pengecualian penting: "berapa tahun X berdiri" bukan permintaan hitung,
    melainkan pertanyaan atribut.

    Pertanyaan yang tidak menyebut satu pun kosakata domain (museum, pameran,
    galeri, provinsi, kota, tema, era, atau nama entitas di graf) ditandai
    ``tidak_dikenal``. Tanpa penjagaan ini, kata "berapa" pada "berapa harga
    tiket pesawat?" akan dibaca sebagai permintaan hitung dan dijawab dengan
    jumlah museum — jawaban benar untuk pertanyaan yang salah.
    """
    teks = _bersih(pertanyaan)
    kata = bersihkan_kata(teks)

    if not teks:
        return Intent("tidak_dikenal", "-", kata=[], alasan="Pertanyaan kosong.")

    # Pertanyaan di luar kemampuan graf ditolak lebih dulu. Satu kata domain
    # ("ke Aceh", "museum") tidak boleh membuka pintu bagi pertanyaan yang
    # datanya tidak pernah disimpan di sini.
    luar = [k for k in _DI_LUAR_DOMAIN if k in teks]
    if luar:
        return Intent(
            "tidak_dikenal",
            "-",
            kata=kata,
            alasan=(
                f"Pertanyaan menyebut hal yang tidak disimpan di graf "
                f"({', '.join(luar)}). Graf hanya memuat fakta museum: lokasi, "
                "tema, era, pameran, dan foto."
            ),
        )

    atribut = None
    if re.search(
        r"(?:tahun|kapan)\b.{0,60}?\b(?:berdiri|didirikan|diresmikan|berdirinya)", teks
    ):
        atribut = "establishedYear"
    elif _ada_kata(teks, "alamat"):
        atribut = "address"
    elif re.search(r"(?:ukuran|jumlah)\s+koleksi", teks):
        atribut = "collectionSize"

    hitung = any(_ada_kata(teks, k) for k in _HITUNG) and atribut is None
    if atribut == "establishedYear":
        hitung = False

    topik = None
    for nama, kunci in _TOPIK:
        if any(_ada_kata(teks, k) for k in kunci):
            topik = nama
            break

    jangkar = None
    if store is not None:
        temuan = cari_jangkar(store, teks, maks=1)
        if temuan:
            jangkar = temuan[0].iri

    # Domain graf adalah museum; kata "museum" sendiri dihitung sebagai topik.
    menyebut_museum = _ada_kata(teks, "museum")
    if topik is None and menyebut_museum:
        topik = "museum"

    # Jangkar saja tidak cukup untuk menentukan topik: "berapa kota di Sumatera"
    # menemukan jangkar "Sumatera" tetapi tidak boleh dibaca sebagai hitung
    # museum. Tanpa topik, topik diwarisi dari jenis jangkar.
    if topik is None and jangkar is not None and store is not None:
        jenis_jangkar = _jenis_jangkar(store, jangkar)
        if jenis_jangkar in ("kota", "provinsi", "museum"):
            topik = "museum" if jenis_jangkar == "museum" else jenis_jangkar

    if topik is None and atribut is None:
        return Intent(
            "tidak_dikenal",
            "-",
            kata=kata,
            jangkar=jangkar,
            alasan=(
                "Pertanyaan tidak menyebut museum, pameran, galeri, provinsi, "
                "kota, tema, era, maupun nama entitas di graf."
            ),
        )

    topik = topik or "museum"

    if atribut:
        jenis = "atribut"
    elif hitung:
        jenis = "hitung"
    else:
        jenis = "daftar"

    return Intent(
        jenis=jenis,
        topik=topik,
        jangkar=jangkar,
        atribut=atribut,
        kata=kata,
        alasan=f"jenis={jenis}, topik={topik}",
    )


# --------------------------------------------------------------- pencetakan


def ke_sparql(
    pertanyaan: str,
    store: MuseumStore,
    llm: Callable[[str], str] | None = None,
) -> str:
    """Terjemahkan pertanyaan menjadi query SPARQL."""
    if llm is not None:
        return llm(prompt(pertanyaan, store))
    return _rakit(pertanyaan, store)


def prompt(pertanyaan: str, store: MuseumStore) -> str:
    """Prompt NL2SPARQL berisi skema, contoh, dan aturan (P13 bagian 15).

    Memakai ``str.replace``, bukan ``str.format`` — kurawal SPARQL akan dibaca
    ``format`` sebagai placeholder dan memicu ``KeyError``.
    """
    skema = skema_graf(store).teks()
    contoh = (
        "T: Museum apa saja yang ada di Aceh?\n"
        "Q: SELECT ?nama WHERE { ?m a sdp:Museum ; rdfs:label ?nama ; "
        'sdp:locatedInProvince ?p . ?p rdfs:label "Aceh" } LIMIT 50\n'
        "T: Berapa jumlah museum?\n"
        "Q: SELECT (COUNT(?m) AS ?n) WHERE { ?m a sdp:Museum } LIMIT 50"
    )
    template = (
        "Terjemahkan pertanyaan ke SPARQL untuk graf museum Sumatera.\n\n"
        "# SKEMA: hanya IRI berikut yang boleh dipakai\n{skema}\n\n"
        "# CONTOH\n{contoh}\n\n"
        "# ATURAN\nQuery saja, tanpa penjelasan.\nHanya SELECT.\n"
        "Selalu LIMIT <= 50.\n\n"
        "T: {pertanyaan}\nQ:"
    )
    return (
        template.replace("{skema}", skema)
        .replace("{contoh}", contoh)
        .replace("{pertanyaan}", pertanyaan)
    )


def _jenis_jangkar(store: MuseumStore, iri: Any) -> str:
    """Tentukan jenis entitas jangkar dari tipenya di graf."""
    from rdflib.namespace import RDF

    node = URIRef(str(iri))
    if (node, RDF.type, SDP.City) in store.asserted:
        return "kota"
    if (node, RDF.type, SDP.Province) in store.asserted:
        return "provinsi"
    if (node, RDF.type, SDP.Museum) in store.asserted:
        return "museum"
    return "-"


def _properti_ada(store: MuseumStore, *nama: str) -> bool:
    """Apakah semua properti `sdp:<nama>` benar-benar dipakai di graf.

    Penerjemah tidak boleh mengarang IRI: query yang memakai properti yang tidak
    ada akan ditolak guard ("IRI tidak dikenal"), dan pengguna melihat penolakan
    atas query buatan sistem sendiri. Graf yang lebih kecil dari data lengkap
    (mis. graf uji) tetap harus bisa ditanyai.
    """
    predikat = {p for _, p, _ in store.asserted}
    return all(SDP[n] in predikat for n in nama)


def _rakit(pertanyaan: str, store: MuseumStore) -> str:
    """Rakit query dari intent (penerjemah berbasis aturan)."""
    niat = intent(pertanyaan, store)
    jangkar = f"<{niat.jangkar}>" if niat.jangkar else None

    if niat.jenis == "tidak_dikenal":
        return ""

    # --- atribut: nilai tunggal sebuah museum -------------------------------
    if niat.jenis == "atribut" and niat.atribut:
        if jangkar:
            return (
                f"{PREFIXES}\nSELECT ?nilai WHERE {{\n"
                f"  {jangkar} sdp:{niat.atribut} ?nilai .\n}}\nLIMIT 50"
            )
        return (
            f"{PREFIXES}\nSELECT ?nama ?nilai WHERE {{\n"
            f"  ?m a sdp:Museum ; {NAMA} ?nama ; sdp:{niat.atribut} ?nilai .\n"
            f"}}\nLIMIT 50"
        )

    # --- hitung ------------------------------------------------------------
    if niat.jenis == "hitung":
        if niat.topik == "pameran":
            pola = "  ?m a sdp:Museum ; sdp:hasExhibit ?x ."
        elif niat.topik == "galeri":
            pola = "  ?m a sdp:Museum ; sdp:hasImage ?x ."
        elif niat.topik == "provinsi":
            pola = "  ?x a sdp:Province ."
        elif niat.topik == "kota":
            pola = "  ?x a sdp:City ."
        elif niat.topik == "tema":
            pola = "  ?x a sdp:Theme ."
        elif niat.topik == "era":
            pola = "  ?x a sdp:Era ."
        else:
            pola = "  ?x a sdp:Museum ."

        # Jangkar harus mempersempit hitungan. Tanpa ini, "berapa pameran di
        # Museum X" menghitung pameran seluruh graf — angka benar untuk
        # pertanyaan yang salah.
        sempit: list[str] = []
        if jangkar and niat.topik in ("pameran", "galeri"):
            relasi = "hasExhibit" if niat.topik == "pameran" else "hasImage"
            pola = f"  {jangkar} sdp:{relasi} ?x ."
        elif jangkar and niat.topik == "museum":
            jenis = _jenis_jangkar(store, niat.jangkar)
            if jenis == "provinsi":
                if _properti_ada(store, "locatedInProvince"):
                    sempit.append(f"  ?x sdp:locatedInProvince {jangkar} .")
                if _properti_ada(store, "locatedInCity", "partOfProvince"):
                    sempit.append(
                        f"  ?x (sdp:locatedInProvince|"
                        f"(sdp:locatedInCity/sdp:partOfProvince)) {jangkar} ."
                    )
                # Cukup satu jalur: pakai union path bila tersedia.
                if len(sempit) > 1:
                    sempit = [sempit[1]]
            elif jenis == "kota" and _properti_ada(store, "locatedInCity"):
                sempit.append(f"  ?x sdp:locatedInCity {jangkar} .")
            elif jenis == "tema" and _properti_ada(store, "hasTheme"):
                sempit.append(f"  ?x sdp:hasTheme {jangkar} .")
            elif jenis == "era" and _properti_ada(store, "hasEra"):
                sempit.append(f"  ?x sdp:hasEra {jangkar} .")
        elif jangkar and niat.topik == "provinsi":
            pola = f"  ?x a sdp:Province . FILTER(?x = {jangkar})"
        elif jangkar and niat.topik == "kota":
            pola = f"  ?x a sdp:City . FILTER(?x = {jangkar})"
        elif jangkar and niat.topik == "tema":
            pola = f"  ?x a sdp:Theme . FILTER(?x = {jangkar})"
        elif jangkar and niat.topik == "era":
            pola = f"  ?x a sdp:Era . FILTER(?x = {jangkar})"

        badan = pola + ("\n" + "\n".join(sempit) if sempit else "")
        return (
            f"{PREFIXES}\nSELECT (COUNT(DISTINCT ?x) AS ?jumlah) WHERE {{\n"
            f"{badan}\n}}\nLIMIT 50"
        )

    # --- daftar pameran / galeri -------------------------------------------
    if niat.topik == "pameran":
        pola = (
            f"  ?m a sdp:Museum ; {NAMA} ?museum ; sdp:hasExhibit ?x .\n"
            "  ?x sdp:exhibitTitle ?judul ."
        )
        if jangkar:
            pola = f"  {jangkar} sdp:hasExhibit ?x .\n  ?x sdp:exhibitTitle ?judul ."
        return (
            f"{PREFIXES}\nSELECT ?x ?judul WHERE {{\n{pola}\n}}"
            "\nORDER BY ?judul\nLIMIT 50"
        )

    if niat.topik == "galeri":
        pola = f"  ?m a sdp:Museum ; sdp:hasImage ?x .\n  ?x sdp:imageTitle ?judul ."
        if jangkar:
            pola = f"  {jangkar} sdp:hasImage ?x .\n  ?x sdp:imageTitle ?judul ."
        return (
            f"{PREFIXES}\nSELECT ?x ?judul WHERE {{\n{pola}\n}}"
            "\nORDER BY ?judul\nLIMIT 50"
        )

    # --- daftar museum -----------------------------------------------------
    pola = [
        "  ?museum a sdp:Museum ;",
        f"          {NAMA} ?nama .",
    ]
    if _properti_ada(store, "locatedInCity"):
        pola.append(
            f"  OPTIONAL {{ ?museum sdp:locatedInCity ?kotaNode . ?kotaNode {NAMA} ?kota }}"
        )
    if _properti_ada(store, "locatedInProvince"):
        pola.append(
            f"  OPTIONAL {{ ?museum sdp:locatedInProvince ?provNode . ?provNode {NAMA} ?provinsi }}"
        )
    if _properti_ada(store, "establishedYear"):
        pola.append("  OPTIONAL { ?museum sdp:establishedYear ?tahun }")
    saring: list[str] = []
    if jangkar:
        jenis = _jenis_jangkar(store, niat.jangkar)
        if jenis == "kota" and _properti_ada(store, "locatedInCity"):
            saring.append(f"  ?museum sdp:locatedInCity {jangkar} .")
        elif jenis == "museum":
            saring.append(f"  ?museum sdp:relatedMuseum {jangkar} .")
        elif _properti_ada(store, "locatedInProvince") and _properti_ada(
            store, "locatedInCity", "partOfProvince"
        ):
            # Provinsi: museum bisa menunjuk provinsi langsung **atau** lewat
            # kotanya (multi-hop). Property path menangani keduanya.
            saring.append(
                f"  ?museum (sdp:locatedInProvince|"
                f"(sdp:locatedInCity/sdp:partOfProvince)) {jangkar} ."
            )
        elif _properti_ada(store, "locatedInProvince"):
            saring.append(f"  ?museum sdp:locatedInProvince {jangkar} .")
        elif _properti_ada(store, "locatedInCity"):
            saring.append(f"  ?museum sdp:locatedInCity {jangkar} .")

    terpakai = {
        "museum", "yang", "di", "ada", "apa", "saja", "semua", "kota", "provinsi", "berapa",
    }
    if niat.jangkar:
        terpakai |= set(store.nama(URIRef(niat.jangkar)).lower().split())

    for kata_kunci in niat.kata:
        bersih_kata = kata_kunci.lower().strip("?.!,;:")
        if not bersih_kata or bersih_kata in terpakai:
            continue
        saring.append(
            f"  FILTER(CONTAINS(LCASE(STR(?nama)), LCASE({literal(bersih_kata)})))"
        )

    badan = "\n".join(pola + saring)
    return (
        f"{PREFIXES}\n"
        "SELECT DISTINCT ?museum ?nama ?kota ?provinsi ?tahun\n"
        f"WHERE {{\n{badan}\n}}\n"
        "ORDER BY LCASE(STR(?nama))\nLIMIT 50"
    )


# ------------------------------------------------------------------- guard


def _iri_di(algebra: Any) -> Iterable[URIRef]:
    """Telusuri pohon algebra query dan kembalikan setiap ``URIRef``.

    rdflib menyusun query sebagai ``CompValue`` bersarang. Penelusuran harus
    masuk ke **semua** kunci, karena properti karangan bisa muncul di posisi
    predikat, di ``FILTER``, maupun di dalam **property path**.

    Property path direpresentasikan sebagai ``rdflib.paths.Path`` yang bentuk
    internalnya berbeda-beda, dan inilah yang dulu membuat pemeriksaan keempat
    bisa dilewati:

    - ``SequencePath``/``AlternativePath``/``NegatedPath`` menyimpan isinya di ``args``
    - ``MulPath`` (``+ * ?``) menyimpan IRI di ``path``
    - ``InvPath`` (``^``) menyimpan IRI di ``arg``

    Karena itu penelusuran di sini tidak mengandalkan satu nama kunci saja.
    """
    if algebra is None:
        return
    if isinstance(algebra, URIRef):
        yield algebra
        return
    if isinstance(algebra, (str, bytes)):
        return
    if isinstance(algebra, (list, tuple, set)):
        for item in algebra:
            yield from _iri_di(item)
        return

    # Property path: tangani lebih dulu, sebelum cabang generik di bawah.
    if isinstance(algebra, Path):
        for kunci in ("args", "path", "arg", "iri"):
            nilai = getattr(algebra, kunci, None)
            if nilai is not None:
                yield from _iri_di(nilai)
        return

    if hasattr(algebra, "keys") and hasattr(algebra, "values"):
        for nilai in algebra.values():
            yield from _iri_di(nilai)
        # `CompValue` menyimpan sebagian simpul di atribut, bukan di kunci.
        for kunci in ("args", "path", "arg", "iri", "expr", "term"):
            nilai = getattr(algebra, kunci, None)
            if nilai is not None:
                yield from _iri_di(nilai)
        return
    iteratif = getattr(algebra, "__iter__", None)
    if callable(iteratif):
        try:
            for item in algebra:
                yield from _iri_di(item)
        except TypeError:
            return


def _slice_di(algebra: Any) -> tuple[list[Any], int]:
    """Kumpulkan setiap simpul ``Slice`` dan hitung jumlah subquery.

    Pemeriksaan hanya pada ``algebra.p`` melewatkan subquery: query luar boleh
    punya ``LIMIT 5`` sementara subquery di dalamnya mengambil seluruh graf.
    Subquery dikenali dari simpul ``ToMultiSet``, karena subquery tanpa LIMIT
    tidak menyisakan simpul ``Slice`` sama sekali.
    """
    hasil: list[Any] = []
    subquery = 0

    def jalan(node: Any, kedalaman: int = 0) -> None:
        nonlocal subquery
        if node is None or kedalaman > 40:
            return
        if isinstance(node, (str, bytes, URIRef)):
            return
        nama = getattr(node, "name", "")
        if nama == "Slice":
            hasil.append(node)
        elif nama == "ToMultiSet":
            subquery += 1
        if isinstance(node, (list, tuple, set)):
            for item in node:
                jalan(item, kedalaman + 1)
            return
        if hasattr(node, "keys") and hasattr(node, "values"):
            for nilai in node.values():
                jalan(nilai, kedalaman + 1)
            for kunci in ("p", "expr", "term", "args", "path", "arg"):
                nilai = getattr(node, kunci, None)
                if nilai is not None:
                    jalan(nilai, kedalaman + 1)

    jalan(algebra)
    return hasil, subquery


def aman(q: str, store: MuseumStore, maks: int = MAKS_LIMIT) -> tuple[bool, str]:
    """Guard: periksa query **sebelum** dijalankan (P13 bagian 16).

    Empat pemeriksaan: sintaks sah, hanya ``SELECT``, ``LIMIT`` ada dan tidak
    melebihi ``maks``, dan semua IRI dikenal.

    Pemeriksaan ``LIMIT`` berlaku untuk **setiap** blok di dalam query, bukan
    hanya blok terluar, supaya subquery tidak bisa dipakai melewati batas.
    ``OFFSET`` juga dibatasi agar tidak bisa dijadikan cara mengambil data
    sangat dalam tanpa melewati ``LIMIT``.

    Yang **tidak** diperiksa: apakah arah relasi sesuai maksud pertanyaan, dan
    apakah pengguna berhak atas data itu.
    """
    if not q or not q.strip():
        return False, "query kosong"

    try:
        algebra = prepareQuery(q, initNs=PREFIX_MAP).algebra
    except Exception as exc:  # noqa: BLE001 - pesan apa adanya untuk pengguna
        return False, f"query tidak sah: {exc.__class__.__name__}"

    nama = getattr(algebra, "name", "")
    if nama != "SelectQuery":
        return False, f"hanya SELECT (ditemukan {nama or 'bukan query'})"

    potongan, jumlah_subquery = _slice_di(algebra)
    if not potongan:
        return False, f"wajib LIMIT <= {maks} berupa angka tetap"
    # Setiap subquery harus punya Slice sendiri; bila tidak, batasnya tak terjaga.
    if len(potongan) < jumlah_subquery + 1:
        return False, f"wajib LIMIT <= {maks} pada setiap blok, termasuk subquery"
    if getattr(algebra.p, "name", "") != "Slice":
        return False, f"wajib LIMIT <= {maks} pada query terluar"

    for simpul in potongan:
        # rdflib menyimpan LIMIT di kunci 'length' dan OFFSET di 'start'.
        batas = simpul.get("length")
        mulai = simpul.get("start")
        if isinstance(batas, str) or hasattr(batas, "name"):
            batas = None
        if batas is None:
            return False, f"wajib LIMIT <= {maks} pada setiap blok, termasuk subquery"
        try:
            nilai_batas = int(batas)
        except (TypeError, ValueError):
            return False, "LIMIT harus bilangan bulat"
        if nilai_batas < 1:
            return False, "LIMIT harus lebih besar dari 0"
        if nilai_batas > maks:
            return False, f"LIMIT {nilai_batas} melebihi batas {maks}"
        if mulai is not None:
            try:
                nilai_mulai = int(mulai)
            except (TypeError, ValueError):
                return False, "OFFSET harus bilangan bulat"
            if nilai_mulai > maks:
                return False, f"OFFSET {nilai_mulai} melebihi batas {maks}"

    dikenal = kosakata(store)
    asing = sorted({str(i) for i in _iri_di(algebra) if str(i) not in dikenal})
    if asing:
        return False, "IRI tidak dikenal: " + ", ".join(asing)

    return True, "ok"


# -------------------------------------------------------------- verbalisasi


@dataclass
class Hasil:
    """Satu jawaban utuh beserta jejak yang membuatnya dapat diperiksa."""

    pertanyaan: str
    query: str
    lolos: bool
    pesan: str
    jawaban: str
    sumber: list[str] = field(default_factory=list)
    baris: list[list[str]] = field(default_factory=list)
    jangkar: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "pertanyaan": self.pertanyaan,
            "query": self.query,
            "lolos": self.lolos,
            "pesan": self.pesan,
            "jawaban": self.jawaban,
            "sumber": self.sumber,
            "baris": self.baris,
            "jangkar": self.jangkar,
        }


def _teks_baris(baris: Iterable[Any]) -> list[str]:
    return [label_slug(str(x)) if isinstance(x, URIRef) else str(x) for x in baris]


def jawab(
    pertanyaan: str,
    store: MuseumStore,
    llm: Callable[[str], str] | None = None,
    penerjemah: Callable[[str], str] | None = None,
) -> Hasil:
    """Alur utuh P13 bagian 24: terjemahkan → validasi → jalankan → verbalisasi.

    Dua peran model dipisah: ``penerjemah`` menulis query, ``llm`` merangkai
    jawaban. Query dari model tetap harus lolos guard.

    Aturan yang dijaga ketat:

    - **Hasil kosong tidak dikirim ke model.**
    - **Query ditolak tidak dijalankan.**
    - **IRI sumber ditempel oleh kode**, bukan oleh model.
    """
    query = ke_sparql(pertanyaan, store, llm=penerjemah)
    ok, pesan = aman(query, store)

    if not ok:
        di_luar_domain = intent(pertanyaan, store).jenis == "tidak_dikenal"
        jawaban = (
            "Pertanyaan ini tidak menyebut apa pun yang ada di graf museum. "
            "Coba sebut nama museum, provinsi, tema, era, pameran, atau foto."
            if di_luar_domain
            else f"Query ditolak ({pesan})."
        )
        return Hasil(
            pertanyaan=pertanyaan,
            query=query,
            lolos=False,
            pesan=pesan,
            jawaban=jawaban,
        )

    baris = list(store.closure.query(query, initNs=PREFIX_MAP))
    if not baris:
        return Hasil(
            pertanyaan=pertanyaan,
            query=query,
            lolos=True,
            pesan="ok",
            jawaban="Tidak ditemukan di graf.",
        )

    data_baris = [[str(x) for x in r] for r in baris]
    konteks = ambil_konteks(store, pertanyaan, hop=1, batas=20)

    # Sumber = IRI entitas yang benar-benar muncul **di hasil query**.
    sumber = sorted(
        {
            str(x)
            for r in baris
            for x in r
            if isinstance(x, URIRef) and "/resource/" in str(x)
        }
    )
    if not sumber:
        # Hitungan/atribut tidak memuat IRI di hasilnya. Sumber diambil dari
        # jangkar yang disebut pertanyaan supaya jawaban tetap dapat ditelusuri.
        sumber = [j["iri"] for j in konteks["jangkar"] if "/resource/" in j["iri"]]

    teks_data = "\n".join(" | ".join(_teks_baris(r)) for r in baris)

    if llm is not None:
        badan = f"{ATURAN_VERBALISASI}\nPertanyaan: {pertanyaan}\nData:\n{teks_data}"
        jawaban = llm(badan).strip()
    else:
        jawaban = _rangkai(pertanyaan, baris, intent(pertanyaan, store))

    if sumber:
        jawaban = jawaban + "\nSumber: " + ", ".join(sumber[:8])

    return Hasil(
        pertanyaan=pertanyaan,
        query=query,
        lolos=True,
        pesan="ok",
        jawaban=jawaban,
        sumber=sumber,
        baris=data_baris,
        jangkar=konteks["jangkar"],
    )


def _rangkai(pertanyaan: str, baris: list[Any], niat: Intent | None = None) -> str:
    """Susun kalimat dari data — tanpa menambah satu fakta pun.

    `niat` diteruskan dari pemanggil: membaca ulang intent di sini tanpa `store`
    akan kehilangan topik dan membuat satuannya salah (mis. "3 entitas" padahal
    yang dihitung museum).
    """
    if niat is None:
        niat = intent(pertanyaan)
    jumlah = len(baris)

    if niat.jenis == "hitung":
        nilai = str(baris[0][0]) if baris and baris[0] else "0"
        satuan = {
            "pameran": "pameran",
            "galeri": "foto",
            "provinsi": "provinsi",
            "kota": "kota",
            "tema": "tema",
            "era": "era",
            "museum": "museum",
        }.get(niat.topik, "entitas")
        return f"Ada {nilai} {satuan} yang tercatat di graf."

    if niat.jenis == "atribut":
        nilai = str(baris[0][0]) if baris and baris[0] else "-"
        label = {
            "establishedYear": "tahun berdiri",
            "address": "alamat",
            "collectionSize": "ukuran koleksi",
        }.get(niat.atribut or "", "nilai")
        return f"{label.capitalize()} menurut graf: {nilai}."

    if niat.topik in ("pameran", "galeri"):
        # Kolom pertama bisa berupa IRI (untuk sumber); judul di kolom terakhir.
        judul = [
            str(r[-1])
            for r in baris
            if r and r[-1] is not None and not str(r[-1]).startswith("http")
        ]
        tampil = judul[:10]
        sisa = len(judul) - len(tampil)
        teks = f"Ditemukan {len(judul)} {niat.topik}: " + "; ".join(tampil)
        if sisa > 0:
            teks += f"; dan {sisa} lainnya"
        return teks + "."

    if jumlah == 1:
        nama = str(baris[0][1]) if len(baris[0]) > 1 else str(baris[0][0])
        return f"Ditemukan 1 museum: {nama}."
    nama = [str(r[1]) for r in baris if len(r) > 1 and r[1] is not None]
    tampil = nama[:10]
    sisa = len(nama) - len(tampil)
    teks = f"Ditemukan {len(nama)} museum: " + "; ".join(tampil)
    if sisa > 0:
        teks += f"; dan {sisa} lainnya"
    return teks + "."
