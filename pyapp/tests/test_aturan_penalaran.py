"""Fakta turunan: bersih, terurut, dan berlabel aturan."""

from pathlib import Path

import pytest
from rdflib import BNode, Graph
from rdflib.namespace import OWL, RDFS

from semweb.reasoning import aturan_fakta, fakta_turunan
from semweb.store import MuseumStore

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
    return MuseumStore.dari_turtle(path=DATA_TTL)


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


def test_312_fakta_dan_218_prp_inv():
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada — angka target tidak terverifikasi")
    fakta = fakta_turunan(store_penuh(), batas=10_000)
    assert len(fakta) == 312
    inv = [f for f in fakta if f["predikat"].endswith("OfMuseum")]
    assert len(inv) == 218


def test_tanpa_ontologi_hanya_28_fakta():
    """Tanpa aksioma ontologi, hanya rdfs9 dari 4 subClassOf di data yang bisa jalan."""
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada")
    store = MuseumStore.dari_turtle(path=DATA_TTL, ontologi="none")
    assert len(fakta_turunan(store, batas=10_000)) == 28


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


def test_semua_312_fakta_teratribusi():
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
