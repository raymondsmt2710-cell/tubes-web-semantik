from rdflib import URIRef

from semweb.reasoning import (
    cek_konsistensi,
    fakta_turunan,
    jelaskan_tipe,
    perbandingan,
)
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

<https://museumsumatera.id/resource/museum/a> a sdp:StateMuseum ;
    sdp:name "Museum A"@id .
sdp:StateMuseum rdfs:subClassOf sdp:Museum .
sdp:Museum rdfs:subClassOf owl:Thing .
"""

MUSEUM_A = URIRef("https://museumsumatera.id/resource/museum/a")


def store():
    return MuseumStore.dari_turtle(data=TTL)


def test_perbandingan_melaporkan_empat_angka():
    p = perbandingan(store())
    assert set(p) >= {"asserted", "closure_owlrl", "closure_rdfs", "inferred"}
    assert p["inferred"] == p["closure_owlrl"] - p["asserted"]


def test_fakta_turunan_tidak_ada_di_asserted():
    s = store()
    turunan = fakta_turunan(s)
    assert turunan, "harus ada fakta turunan"
    asserted = {(str(t[0]), str(t[1]), str(t[2])) for t in s.asserted}
    for f in turunan:
        assert (f["subjek"], f["predikat"], f["objek"]) not in asserted


def test_jelaskan_tipe_menyebut_rantai_subclass():
    rantai = jelaskan_tipe(store(), "a")
    teks = " ".join(rantai)
    assert "StateMuseum" in teks
    assert "Museum" in teks


def test_jelaskan_tipe_menandai_fakta_yang_diturunkan():
    rantai = jelaskan_tipe(store(), "a")
    assert any("diturunkan" in kalimat.lower() for kalimat in rantai)


def test_fakta_turunan_bisa_dibatasi_per_subjek():
    s = store()
    turunan = fakta_turunan(s, subjek=MUSEUM_A)
    assert turunan
    assert all(f["subjek"].endswith("/museum/a") for f in turunan)


def test_cek_konsistensi_kosong_untuk_graf_sehat():
    assert cek_konsistensi(store()) == []


def test_cek_konsistensi_menemukan_kelas_disjoint():
    ttl = TTL + """
sdp:StateMuseum owl:disjointWith sdp:PrivateMuseum .
<https://museumsumatera.id/resource/museum/b> a sdp:StateMuseum, sdp:PrivateMuseum .
"""
    pesan = cek_konsistensi(MuseumStore.dari_turtle(data=ttl))
    assert pesan
    assert any("PrivateMuseum" in p for p in pesan)


def test_fakta_turunan_tidak_memuat_sameas_refleksif():
    """Artefak reasoner (x owl:sameAs x) bukan pengetahuan baru bagi pembaca."""
    turunan = fakta_turunan(store())
    assert turunan
    for f in turunan:
        if f["predikat"].endswith("sameAs"):
            assert f["subjek"] != f["objek"]


def test_fakta_turunan_tidak_memuat_objek_trivial():
    turunan = fakta_turunan(store())
    for f in turunan:
        assert not f["objek"].endswith("owl#Thing")
        assert not f["objek"].endswith("rdf-schema#Resource")


def test_jelaskan_tipe_untuk_slug_tidak_dikenal():
    pesan = jelaskan_tipe(store(), "tidak-ada")
    assert pesan
    assert "tidak ada" in pesan[0].lower()
