"""Test regresi untuk temuan review yang sebelumnya ditunda (minor).

Setiap test di sini mengunci satu perilaku yang dulu salah, supaya tidak
kembali diam-diam.
"""

import pytest
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD

from semweb.namespace import RES, SDP
from semweb.reasoning import cek_konsistensi
from semweb.relations import kueri_benang_merah
from semweb.search import kueri_cari
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://museumsumatera.id/resource/museum/a> a sdp:StateMuseum ;
    sdp:name "Museum A"@id ;
    sdp:establishedYear "1915"^^xsd:gYear ;
    sdp:collectionSize 100 .
sdp:StateMuseum rdfs:subClassOf sdp:Museum .
sdp:Museum rdfs:subClassOf owl:Thing .
"""


@pytest.fixture
def store():
    return MuseumStore.dari_turtle(data=TTL)


# --- D: tahun_min pada xsd:gYear ------------------------------------------


def test_filter_tahun_min_tidak_memanggil_integer_pada_gYear_langsung():
    """`xsd:integer()` pada literal `xsd:gYear` bisa error di engine ketat.

    Nilainya harus diubah lewat `STR()` lebih dulu, atau dibandingkan langsung
    dengan `xsd:gYear`.
    """
    q = kueri_cari(tahun_min=1980)
    assert "xsd:integer(STR(?tahun))" not in q
    # Perbandingan tetap ada dan memakai 1980.
    assert "1980" in q
    assert "?tahun" in q


def test_tahun_min_tetap_menyaring(store):
    from semweb.search import cari_museum

    assert [m["slug"] for m in cari_museum(store, tahun_min=1980)] == []
    assert [m["slug"] for m in cari_museum(store, tahun_min=1900)] == ["a"]


# --- K: highlight boolean ------------------------------------------------


def test_exhibit_highlight_string_false_tidak_dibaca_true():
    """`Literal("false")` bernilai truthy di Python; harus dibaca sebagai False."""
    from main import _museum_dto

    ttl = TTL + """
res:ex a sdp:Exhibit ;
    sdp:exhibitIndex 1 ;
    sdp:exhibitTitle "Bukan andalan"@id ;
    sdp:exhibitHighlight "false"^^xsd:boolean .
<https://museumsumatera.id/resource/museum/a> sdp:hasExhibit res:ex .
"""
    s = MuseumStore.dari_turtle(data=ttl)
    dto = _museum_dto(s, URIRef(f"{RES}museum/a"))
    assert dto["exhibits"][0]["andalan"] is False


def test_exhibit_highlight_true_dibaca_true():
    from main import _museum_dto

    ttl = TTL + """
res:ex a sdp:Exhibit ;
    sdp:exhibitIndex 1 ;
    sdp:exhibitTitle "Andalan"@id ;
    sdp:exhibitHighlight true .
<https://museumsumatera.id/resource/museum/a> sdp:hasExhibit res:ex .
"""
    s = MuseumStore.dari_turtle(data=ttl)
    dto = _museum_dto(s, URIRef(f"{RES}museum/a"))
    assert dto["exhibits"][0]["andalan"] is True


# --- J: establishedYear bukan angka polos --------------------------------


def test_tahun_berformat_tanggal_tidak_melempar_error():
    """`xsd:gYear` bisa berisi "1915-01-01"; `int()` polos akan melempar."""
    from main import _museum_dto

    ttl = TTL.replace('"1915"^^xsd:gYear', '"1915-01-01"^^xsd:gYear')
    s = MuseumStore.dari_turtle(data=ttl)
    dto = _museum_dto(s, URIRef(f"{RES}museum/a"))
    assert dto["tahun"] in (1915, None)


# --- I: fallback nama -----------------------------------------------------


def test_nama_kosong_memakai_label_bisa_dibaca():
    """Jangan tampilkan slug mentah seperti "museum-negeri-aceh"."""
    from main import _museum_dto

    ttl = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
<https://museumsumatera.id/resource/museum/museum-negeri-aceh> a sdp:Museum .
"""
    s = MuseumStore.dari_turtle(data=ttl)
    dto = _museum_dto(s, URIRef(f"{RES}museum/museum-negeri-aceh"))
    assert dto["nama"] != "museum-negeri-aceh"
    assert "Museum" in dto["nama"] or "Negeri" in dto["nama"]


# --- P: maks dipakai di kueri benang merah --------------------------------


def test_kueri_benang_merah_memakai_batas_di_dalam_query():
    """`maks` harus benar-benar dipakai, bukan parameter yang diabaikan."""
    kecil = kueri_benang_merah("museum-a", 2)
    besar = kueri_benang_merah("museum-a", 9)
    assert kecil != besar
    assert "2" in kecil


# --- R: konsistensi juga memeriksa closure --------------------------------


def test_cek_konsistensi_menangkap_pelanggaran_akibat_inferensi():
    """Kelas disjoint yang terpenuhi lewat `rdfs:subClassOf` juga dilaporkan."""
    ttl = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

sdp:StateMuseum rdfs:subClassOf sdp:Museum .
sdp:Museum owl:disjointWith sdp:PrivateMuseum .
sdp:PrivateMuseum rdfs:subClassOf sdp:Museum .

<https://museumsumatera.id/resource/museum/x> a sdp:StateMuseum, sdp:PrivateMuseum .
"""
    s = MuseumStore.dari_turtle(data=ttl)
    assert cek_konsistensi(s), "pelanggaran disjoint harus dilaporkan"


def test_cek_konsistensi_masih_kosong_untuk_graf_sehat(store):
    assert cek_konsistensi(store) == []
