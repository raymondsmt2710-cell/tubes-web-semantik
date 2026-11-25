from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF

from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<https://museumsumatera.id/resource/museum/a> a sdp:Museum, sdp:StateMuseum ;
    sdp:name "Museum A"@id ;
    sdp:locatedInCity res:city-x .
res:city-x a sdp:City ;
    sdp:partOfProvince res:province-aceh .
res:province-aceh a sdp:Province .

sdp:StateMuseum rdfs:subClassOf sdp:Museum .
sdp:Museum rdfs:subClassOf owl:Thing .
"""

MUSEUM_A = URIRef("https://museumsumatera.id/resource/museum/a")


def store_contoh() -> MuseumStore:
    return MuseumStore.dari_turtle(data=TTL)


def test_asserted_hanya_berisi_triple_yang_ditulis():
    s = store_contoh()
    assert len(s.asserted) == len(Graph().parse(data=TTL, format="turtle"))


def test_closure_lebih_besar_dari_asserted():
    s = store_contoh()
    assert len(s.closure) > len(s.asserted)


def test_closure_menyimpulkan_tipe_superclass():
    s = store_contoh()
    assert (MUSEUM_A, RDF.type, OWL.Thing) in s.closure


def test_asserted_tidak_ikut_berubah_setelah_closure():
    """Reasoner tidak mengubah fakta yang ditulis — aturan materi P12."""
    s = store_contoh()
    assert (MUSEUM_A, RDF.type, OWL.Thing) not in s.asserted


def test_ringkasan_melaporkan_jumlah_triple_asserted_dan_closure():
    s = store_contoh()
    r = s.ringkasan()
    assert r["asserted"] == len(s.asserted)
    assert r["closure"] == len(s.closure)
    assert r["inferred"] == r["closure"] - r["asserted"]
    assert r["inferred"] > 0


def test_cari_iri_menemukan_museum_berdasarkan_nama():
    s = store_contoh()
    assert MUSEUM_A in s.cari_iri("Museum A")


def test_cari_iri_tidak_peka_huruf_besar_kecil():
    s = store_contoh()
    assert MUSEUM_A in s.cari_iri("museum a")


def test_nama_mengembalikan_label_bukan_iri():
    s = store_contoh()
    assert s.nama(MUSEUM_A) == "Museum A"
