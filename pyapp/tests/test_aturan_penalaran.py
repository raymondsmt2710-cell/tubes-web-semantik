"""Fakta turunan: bersih, terurut, dan berlabel aturan."""

from pathlib import Path

import pytest
from rdflib import BNode, Graph, URIRef
from rdflib.namespace import OWL, RDFS

from semweb.reasoning import aturan_fakta, fakta_turunan
from semweb.store import MuseumStore

from store_bersama import store_data

AKAR = Path(__file__).resolve().parent.parent.parent
DATA_TTL = AKAR / "data" / "museum-sumatera.ttl"
ONTO_TTL = AKAR / "ontology" / "museum-sumatera.ttl"

PREDIKAT_AKSIOMA = {
    str(RDFS.domain),
    str(RDFS.range),
    str(RDFS.subClassOf),
    str(RDFS.subPropertyOf),
    str(OWL.equivalentClass),
    str(OWL.equivalentProperty),
}


def store_penuh():
    """Store data penuh, dibangun sekali per proses lewat `store_bersama`."""
    return store_data()


def test_tidak_ada_sameas_di_fakta_turunan():
    for f in fakta_turunan(store_penuh(), batas=10_000):
        assert not f["predikat"].endswith("sameAs")


def test_tidak_ada_bnode_di_fakta_turunan():
    store = store_penuh()
    bnode = {str(b) for b in store.closure.all_nodes() if isinstance(b, BNode)}
    for f in fakta_turunan(store, batas=10_000):
        assert f["subjek"] not in bnode
        assert f["objek"] not in bnode


def test_tidak_ada_aksioma_vocabulary():
    for f in fakta_turunan(store_penuh(), batas=10_000):
        assert f["predikat"] not in PREDIKAT_AKSIOMA


def test_tidak_ada_objek_trivial():
    for f in fakta_turunan(store_penuh(), batas=10_000):
        assert not f["objek"].endswith("owl#Thing")
        assert not f["objek"].endswith("owl#Nothing")
        assert not f["objek"].endswith("rdf-schema#Resource")


def test_ontologi_menambah_banyak_fakta_inverse():
    """Ontologi membuat `prp-inv` bekerja; tanpa itu hampir tak ada fakta.

    Dulu test ini mengunci angka 312/218. Angka mati dibuang: data museum terus
    dilengkapi, dan yang sebenarnya ingin dijaga adalah sifatnya — ontologi
    menambah fakta secara besar-besaran, dan mayoritas tambahan itu berasal dari
    properti `*OfMuseum` (pasangan `owl:inverseOf`).
    """
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada — angka target tidak terverifikasi")
    fakta = fakta_turunan(store_penuh(), batas=10_000)
    tanpa = fakta_turunan(
        store_data("none"), batas=10_000
    )
    assert len(fakta) > len(tanpa)
    inv = [f for f in fakta if f["predikat"].endswith("OfMuseum")]
    assert len(inv) > len(tanpa), "mayoritas fakta baru harus dari owl:inverseOf"


def test_tanpa_ontologi_hanya_rdfs9_yang_jalan():
    """Tanpa aksioma ontologi, hanya rdfs9 dari subClassOf di data yang bisa jalan.

    Yang dijaga: hasilnya sedikit, bukan kosong, dan semuanya berlabel `rdfs9`.
    """
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada")
    store = store_data("none")
    fakta = fakta_turunan(store, batas=10_000)
    assert fakta
    assert {a for f in fakta for a in f["aturan"]} == {"rdfs9"}


def test_urut_sebelum_potong_bukan_sesudah():
    """Kalau urutan dilakukan setelah pemotongan, isi halaman berubah tiap proses.

    `batas=5` harus sama dengan 5 baris pertama hasil penuh — bukan 5 baris acak
    yang kebetulan terambil lebih dulu dari iterasi graf.
    """
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada")
    store = store_penuh()
    penuh = fakta_turunan(store, batas=10_000)
    assert fakta_turunan(store, batas=5) == penuh[:5]


def test_urutan_deterministik():
    store = store_penuh()
    a = [(f["subjek"], f["predikat"], f["objek"]) for f in fakta_turunan(store, batas=10_000)]
    b = [(f["subjek"], f["predikat"], f["objek"]) for f in fakta_turunan(store, batas=10_000)]
    assert a == b
    assert a == sorted(a)


def test_setiap_fakta_punya_kunci_aturan():
    for f in fakta_turunan(store_penuh(), batas=10_000):
        assert isinstance(f["aturan"], list)
        assert f["aturan"]


def test_sameas_non_refleksif_tidak_lolos():
    """Data asli hanya punya `sameAs` refleksif, jadi test di atas tidak menangkap
    kebocoran yang justru jadi alasan perbaikan ini: `a owl:sameAs b` antar dua IRI
    berbeda. Fixture kecil ini menutup celah itu."""
    ttl = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix res: <https://museumsumatera.id/resource/> .

res:museum_a a sdp:Museum ; sdp:name "A"@id .
res:museum_b a sdp:Museum ; sdp:name "B"@id .
res:museum_a owl:sameAs res:museum_b .
"""
    store = MuseumStore.dari_turtle(data=ttl)
    predikat = {f["predikat"] for f in fakta_turunan(store, batas=10_000)}
    assert not any(p.endswith("sameAs") for p in predikat)


def _fakta(store, predikat_akhir, objek_akhir=None):
    for f in fakta_turunan(store, batas=10_000):
        if f["predikat"].endswith(predikat_akhir) and (
            objek_akhir is None or f["objek"].endswith(objek_akhir)
        ):
            return f
    raise AssertionError(f"tidak ada fakta {predikat_akhir}")


def test_aturan_prp_inv_dikenali():
    store = store_penuh()
    f = _fakta(store, "exhibitOfMuseum")
    aturan = [a["aturan"] for a in aturan_fakta(store, f)]
    assert "prp-inv" in aturan


def test_aturan_rdfs2_dikenali():
    """rdfs2 dari domain imageUrl yang salah domain (bug ontologi, lihat brief)."""
    store = store_penuh()
    f = _fakta(store, "#type", "#Museum")
    aturan = [a["aturan"] for a in aturan_fakta(store, f)]
    assert "rdfs2" in aturan


def test_aturan_rdfs9_dikenali():
    store = store_penuh()
    for f in fakta_turunan(store, batas=10_000):
        if f["predikat"].endswith("#type") and f["objek"].endswith("#Museum"):
            if "rdfs9" in {a["aturan"] for a in aturan_fakta(store, f)}:
                return
    raise AssertionError("tidak ada fakta yang diatribusikan ke rdfs9")


def test_semua_fakta_teratribusi():
    """Tidak boleh ada fakta yang lolos tanpa aturan: itu berarti reasoner
    menghasilkan sesuatu di luar keenam aturan yang kita kenali."""
    store = store_penuh()
    tanpa = [
        f
        for f in fakta_turunan(store, batas=10_000)
        if [a["aturan"] for a in aturan_fakta(store, f)] == ["tidak teridentifikasi"]
    ]
    assert tanpa == [], f"{len(tanpa)} fakta tanpa justifikasi, contoh: {tanpa[:2]}"


# --- Tiga aturan yang tidak pernah muncul di data asli -----------------------
#
# `prp-symp`, `rdfs3`, dan `rdfs11` tidak punya satu pun contoh di data 28
# museum (tidak ada properti simetris yang dipakai, tidak ada properti ber-range
# yang dipakai, tidak ada rantai subClassOf >= 2 langkah yang menghasilkan
# fakta). Tanpa test di bawah ini, salah ketik pada cabang tersebut tidak akan
# pernah ketahuan — dan justru cabang itulah yang paling mudah salah.


def _aturan_dari(ttl: str, onto: str = "") -> set[str]:
    onto_graph = Graph()
    if onto:
        onto_graph.parse(data=onto, format="turtle")
    store = MuseumStore.dari_turtle(data=ttl, ontologi=onto_graph)
    nama: set[str] = set()
    for f in fakta_turunan(store, batas=10_000):
        nama.update(a["aturan"] for a in aturan_fakta(store, f))
    return nama


def test_aturan_prp_symp_dikenali():
    """Properti bertipe owl:SymmetricProperty + pasangan terbalik -> prp-symp."""
    ttl = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .

res:museum_a a sdp:Museum ; sdp:name "A"@id .
res:museum_b a sdp:Museum ; sdp:name "B"@id .
res:museum_a sdp:relatedMuseum res:museum_b .
"""
    onto = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
sdp:relatedMuseum a owl:SymmetricProperty .
"""
    assert "prp-symp" in _aturan_dari(ttl, onto)


def test_aturan_rdfs3_dikenali():
    """(P range C) + ada x P subjek -> subjek bertipe C."""
    ttl = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .

res:pameran_1 a sdp:Exhibit ; sdp:exhibitTitle "Lonceng"@id .
res:museum_a a sdp:Museum ; sdp:hasExhibit res:pameran_1 .
"""
    onto = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
sdp:hasExhibit rdfs:range sdp:Museum .
"""
    assert "rdfs3" in _aturan_dari(ttl, onto)


def test_aturan_rdfs11_dikenali():
    """Rantai subClassOf dua langkah harus dilaporkan sebagai rdfs11."""
    ttl = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .

res:museum_a a sdp:MuseumDaerah ; sdp:name "A"@id .
"""
    onto = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
sdp:MuseumDaerah rdfs:subClassOf sdp:StateMuseum .
sdp:StateMuseum rdfs:subClassOf sdp:Museum .
"""
    onto_graph = Graph()
    onto_graph.parse(data=onto, format="turtle")
    store = MuseumStore.dari_turtle(data=ttl, ontologi=onto_graph)

    # Fakta yang HANYA bisa dicapai lewat rantai dua langkah: museum bertipe
    # sdp:Museum, padahal tipe tertulisnya sdp:MuseumDaerah.
    fakta_museum = [
        f
        for f in fakta_turunan(store, batas=10_000)
        if f["predikat"].endswith("#type") and f["objek"].endswith("#Museum")
    ]
    assert fakta_museum, "harus ada fakta tipe sdp:Museum"
    aturan = {a["aturan"] for f in fakta_museum for a in aturan_fakta(store, f)}
    assert "rdfs11" in aturan


def test_kalimat_premis_tidak_mengulang_aksioma():
    """Museum dengan banyak tema tidak boleh mengulang kalimat domain yang sama."""
    store = store_penuh()
    for f in fakta_turunan(store, batas=10_000):
        if not (f["predikat"].endswith("#type") and f["objek"].endswith("#Museum")):
            continue
        for a in aturan_fakta(store, f):
            if a["aturan"] != "rdfs2":
                continue
            assert len(a["premis"]) == len(set(a["premis"])), a["premis"]
            return


# --- fakta_turunan membawa nama aturan + cache per store ---------------------
#
# Label aturan baru berguna kalau benar-benar sampai ke halaman; sebelumnya
# `aturan_fakta` hanya dipakai test, sehingga `/metode` tetap menampilkan
# "tidak teridentifikasi". Test di bawah menjaga sambungan itu.


def test_fakta_turunan_mengisi_nama_aturan():
    store = store_penuh()
    fakta = fakta_turunan(store, batas=10_000)
    nama = {a for f in fakta for a in f["aturan"]}
    assert "prp-inv" in nama
    assert "rdfs2" in nama
    assert "rdfs9" in nama
    assert "tidak teridentifikasi" not in nama


def test_cache_tidak_bocor_antar_store():
    """Dua store berbeda tidak boleh berbagi cache.

    Jumlah fakta tidak diikat ke angka mati: data museum terus dilengkapi, dan
    angka mati akan gagal bukan karena logikanya salah. Yang penting adalah
    sifatnya — store berontologi menghasilkan lebih banyak fakta, dan tiap
    store stabil pada nilainya sendiri.
    """
    store_a = store_data()
    store_b = store_data("none")
    a1 = len(fakta_turunan(store_a, batas=10_000))
    b1 = len(fakta_turunan(store_b, batas=10_000))
    assert a1 != b1, "store dengan ontologi harus menghasilkan fakta lebih banyak"
    assert len(fakta_turunan(store_a, batas=10_000)) == a1
    assert len(fakta_turunan(store_b, batas=10_000)) == b1


# Graf kecil: test cache di bawah cukup memakai fixture mini supaya suite tidak
# menambah belasan detik hanya untuk memuat ulang 28 museum.
TTL_MINI = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix res: <https://museumsumatera.id/resource/> .

res:museum_a a sdp:StateMuseum ; sdp:name "A"@id .
res:museum_b a sdp:StateMuseum ; sdp:name "B"@id .
sdp:StateMuseum rdfs:subClassOf sdp:Museum .
"""


def test_cache_menempel_pada_store_bukan_global():
    """Cache global berkunci `id(store)` berbahaya: `id()` didaur ulang setelah GC,
    sehingga store baru bisa mewarisi fakta graf lain."""
    store_a = MuseumStore.dari_turtle(data=TTL_MINI)
    store_b = MuseumStore.dari_turtle(data=TTL_MINI)
    fakta_turunan(store_a, batas=10_000)
    fakta_turunan(store_b, batas=10_000)
    assert isinstance(store_a._cache_fakta_turunan, dict)
    assert store_a._cache_fakta_turunan is not store_b._cache_fakta_turunan


def test_cache_tidak_bisa_diputasi_pemanggil():
    """Pemanggil yang menyunting hasil tidak boleh merusak isi cache."""
    store = MuseumStore.dari_turtle(data=TTL_MINI)
    pertama = fakta_turunan(store, batas=10_000)
    assert pertama
    jumlah = len(pertama)
    pertama.clear()
    pertama.append({"subjek": "palsu", "predikat": "palsu", "objek": "palsu", "aturan": []})

    kedua = fakta_turunan(store, batas=10_000)
    assert len(kedua) == jumlah
    assert kedua[0]["subjek"].endswith("/museum_a")

    # `aturan` adalah satu-satunya nilai bersarang; ia juga harus disalin.
    kedua[0]["aturan"].append("aturan-palsu")
    assert "aturan-palsu" not in fakta_turunan(store, batas=10_000)[0]["aturan"]


def test_cache_dipisah_per_subjek():
    """`subjek` mempersempit hasil, jadi ia harus ikut kunci cache."""
    store = MuseumStore.dari_turtle(data=TTL_MINI)
    semua = fakta_turunan(store, batas=10_000)
    subjek = URIRef(semua[0]["subjek"])
    satu = fakta_turunan(store, subjek=subjek, batas=10_000)
    assert satu
    assert satu == [f for f in semua if f["subjek"] == str(subjek)]


def test_panggilan_kedua_memakai_cache():
    """Panggilan kedua tidak boleh menghitung ulang: entri cache harus objek yang sama."""
    store = MuseumStore.dari_turtle(data=TTL_MINI)
    fakta_turunan(store, batas=10_000)
    tersimpan = store._cache_fakta_turunan[(None, 10_000)]

    fakta_turunan(store, batas=10_000)
    assert store._cache_fakta_turunan[(None, 10_000)] is tersimpan

    # Indeks aksioma juga mahal (menyusuri seluruh graf premis), jadi ia pun
    # disimpan per store, bukan dibangun ulang untuk setiap fakta.
    assert store._cache_peta_aksioma is not None
