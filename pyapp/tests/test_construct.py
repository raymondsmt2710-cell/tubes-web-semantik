from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS

from semweb.construct import (
    hierarki_kelas,
    kueri_hierarki,
    kueri_materialisasi,
    materialisasi,
    selisih_construct_select,
    subkelas_museum,
    verifikasi_hierarki,
)
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

sdp:StateMuseum rdfs:subClassOf sdp:Museum .
sdp:SiteMuseum  rdfs:subClassOf sdp:Museum .
sdp:Museum      rdfs:subClassOf sdp:Tempat .
sdp:Kota        rdfs:subClassOf sdp:Tempat .

res:museum-a a sdp:Museum, sdp:StateMuseum ;
    sdp:name "Museum A"@id .
res:museum-b a sdp:Museum .
"""

MUSEUM_A = URIRef("https://museumsumatera.id/resource/museum-a")


def store() -> MuseumStore:
    return MuseumStore.dari_turtle(data=TTL)


# --------------------------------------------------------------- hierarki


def test_subkelas_langsung_museum():
    """Operator ``+`` hanya mengembalikan subkelas, bukan kelas itu sendiri."""
    lokal = [h["lokal"] for h in subkelas_museum(store())]
    assert "StateMuseum" in lokal
    assert "SiteMuseum" in lokal
    assert "Museum" not in lokal


def test_operator_bintang_menyertakan_kelas_awal():
    """``*`` adalah nol langkah atau lebih, jadi kelas awal ikut (P11)."""
    lokal = [h["lokal"] for h in hierarki_kelas(store(), "Museum", "*")]
    assert "Museum" in lokal


def test_operator_tidak_dikenal_ditolak():
    import pytest

    with pytest.raises(ValueError):
        kueri_hierarki("Museum", "!")


def test_hierarki_menyeberang_dua_tingkat():
    """sdp:Museum subClassOf sdp:Tempat, jadi subkelasnya juga subkelas Tempat."""
    lokal = {h["lokal"] for h in hierarki_kelas(store(), "Tempat", "+")}
    assert {"Museum", "StateMuseum", "SiteMuseum", "Kota"} <= lokal


def test_query_hierarki_memuat_prefix_lengkap():
    """PREFIX ditulis lengkap, bukan disuntikkan editor (P10)."""
    q = kueri_hierarki("Museum", "+")
    assert "PREFIX sdp:" in q
    assert "rdfs:subClassOf+" in q


# ------------------------------------------------------------ materialisasi


def test_materialisasi_menghitung_cetakan_ganda():
    """CONSTRUCT mencetak per solution; graf adalah himpunan."""
    _, angka = materialisasi(store())
    assert angka["dicetak"] > 0
    assert angka["sudah_ada"] >= 1
    assert angka["baru"] == angka["dicetak"] - angka["sudah_ada"]
    assert angka["baru"] < angka["dicetak"]


def test_materialisasi_menurunkan_tipe_superkelas():
    """Aturan setara rdfs9 + rdfs11: tipe superkelas sedalam apa pun."""
    turunan, _ = materialisasi(store())
    tipe = {o for _, _, o in turunan.triples((MUSEUM_A, RDF.type, None))}
    assert URIRef("https://museumsumatera.id/ontology#Tempat") in tipe


def test_query_materialisasi_memakai_construct():
    q = kueri_materialisasi()
    assert "CONSTRUCT" in q
    assert "rdfs:subClassOf+" in q


def test_materialisasi_tidak_mengubah_graf_asserted():
    """Reasoner menambah fakta turunan; fakta yang ditulis tidak diubah (P12)."""
    s = store()
    sebelum = len(s.asserted)
    materialisasi(s)
    assert len(s.asserted) == sebelum


# ------------------------------------------------------ construct vs select


def test_selisih_construct_select():
    """Jumlah baris SELECT dan jumlah triple CONSTRUCT tidak harus sama (P11)."""
    s = store()
    select = """PREFIX sdp: <https://museumsumatera.id/ontology#>
SELECT ?x WHERE { ?x a sdp:Museum }"""
    construct = """PREFIX sdp: <https://museumsumatera.id/ontology#>
CONSTRUCT { ?x a sdp:Museum } WHERE { ?x a sdp:Museum }"""
    hasil = selisih_construct_select(s, select, construct)
    assert hasil["baris_select"] == 2
    assert hasil["triple_construct"] == 2


def test_verifikasi_hierarki_menghitung_individu():
    hasil = {h["lokal"]: h["individu"] for h in verifikasi_hierarki(store())}
    assert hasil["StateMuseum"] == 1
    assert hasil["SiteMuseum"] == 0


def test_hierarki_kelas_kosong_tidak_melempar():
    assert hierarki_kelas(store(), "TidakAda", "+") == []


def test_construct_modul_memakai_namespace_sdp():
    g = Graph().parse(data=TTL, format="turtle")
    assert (URIRef("https://museumsumatera.id/ontology#StateMuseum"), RDFS.subClassOf, None) in g
