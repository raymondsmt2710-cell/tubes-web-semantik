from rdflib import URIRef

from semweb.graphrag import (
    TRIVIAL,
    ambil_konteks,
    jangkar,
    kueri_neighbors,
    kueri_path,
    pola_retrieval,
    triple_konteks,
)
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

sdp:StateMuseum rdfs:subClassOf sdp:Museum .

res:museum-a a sdp:Museum, sdp:StateMuseum ;
    sdp:name "Museum A"@id ;
    sdp:locatedInCity res:city-x ;
    sdp:hasExhibit res:exhibit-1 .

res:museum-b a sdp:Museum ;
    sdp:name "Museum B"@id ;
    sdp:locatedInCity res:city-y .

res:exhibit-1 a sdp:Exhibit ;
    sdp:exhibitTitle "Lonceng Perunggu"@id ;
    sdp:exhibitMaterial "perunggu"@id .

res:city-x a sdp:City ;
    sdp:name "Kota X"@id ;
    sdp:partOfProvince res:prov-aceh .

res:city-y a sdp:City ;
    sdp:name "Kota Y"@id ;
    sdp:partOfProvince res:prov-aceh .

res:prov-aceh a sdp:Province ;
    sdp:name "Aceh"@id .
"""

MUSEUM_A = URIRef("https://museumsumatera.id/resource/museum-a")
PROV_ACEH = URIRef("https://museumsumatera.id/resource/prov-aceh")


def store() -> MuseumStore:
    return MuseumStore.dari_turtle(data=TTL)


# ------------------------------------------------------------------ jangkar


def test_jangkar_menemukan_museum():
    hasil = jangkar(store(), "Apa isi Museum A?")
    assert hasil[0].label == "Museum A"
    assert hasil[0].jenis == "museum"


def test_jangkar_label_panjang_menang():
    """Nama museum lebih spesifik dari nama provinsi, jadi dipilih lebih dulu."""
    hasil = jangkar(store(), "Apa isi Museum A di Aceh?")
    assert hasil[0].label == "Museum A"


def test_jangkar_tidak_cocok_di_dalam_kata_lain():
    """Batas kata: "Aceh" tidak boleh cocok di dalam "Acehnese"."""
    assert jangkar(store(), "budaya Acehnese") == []


def test_jangkar_kosong_untuk_pertanyaan_asing():
    assert jangkar(store(), "berapa harga tiket pesawat") == []


# ------------------------------------------------------------------- subgraf


def test_triple_konteks_mengambil_tetangga_jangkar():
    triple = triple_konteks(store(), [MUSEUM_A], hop=1)
    predikat = {str(p) for _, p, _ in triple}
    assert any(p.endswith("locatedInCity") for p in predikat)
    assert any(p.endswith("hasExhibit") for p in predikat)


def test_triple_konteks_membuang_triple_trivial():
    triple = triple_konteks(store(), [MUSEUM_A], hop=1)
    assert all(o not in TRIVIAL for _, _, o in triple)


def test_triple_konteks_menghormati_batas():
    """Konteks dibatasi supaya seluruh graf tidak dikirim ke model (P13)."""
    triple = triple_konteks(store(), [MUSEUM_A], hop=2, batas=5)
    assert len(triple) <= 5


def test_triple_konteks_tidak_menyedot_seluruh_provinsi():
    """Dari provinsi, penelusuran balik tidak boleh menarik semua museum."""
    triple = triple_konteks(store(), [PROV_ACEH], hop=2)
    subjek = {str(s) for s, _, _ in triple}
    assert not any("museum-b" in s for s in subjek)


def test_konteks_kosong_saat_tidak_ada_jangkar():
    konteks = ambil_konteks(store(), "xyz tidak ada")
    assert konteks["ditemukan"] is False
    assert konteks["triple"] == []
    assert konteks["teks"] == ""


def test_konteks_memuat_sumber_berupa_resource():
    konteks = ambil_konteks(store(), "Museum A")
    assert konteks["ditemukan"] is True
    assert konteks["sumber"]
    assert all("/resource/" in s for s in konteks["sumber"])


# --------------------------------------------------------------- pola query


def test_kueri_neighbors_menghasilkan_construct():
    q = kueri_neighbors(MUSEUM_A, "keduanya")
    assert "CONSTRUCT" in q
    assert "UNION" in q


def test_kueri_neighbors_arah_tidak_dikenal_ditolak():
    import pytest

    with pytest.raises(ValueError):
        kueri_neighbors(MUSEUM_A, "menyamping")


def test_kueri_path_memakai_property_path():
    q = kueri_path(PROV_ACEH, "partOfProvince", "+")
    assert "sdp:partOfProvince+" in q


def test_kueri_path_operator_salah_ditolak():
    import pytest

    with pytest.raises(ValueError):
        kueri_path(PROV_ACEH, "partOfProvince", "!")


def test_pola_retrieval_mencatat_jejak():
    """Tiga pola retrieval GraphRAG beserta query yang dijalankan (P13)."""
    temuan, jejak = pola_retrieval(store(), "Museum A", hop=1)
    assert temuan
    assert jejak
    nama_pola = [j.pola for j in jejak]
    assert any("neighbors" in p for p in nama_pola)
    assert any("structured" in p for p in nama_pola)
    for langkah in jejak:
        assert langkah.query
        assert langkah.keterangan


def test_pola_retrieval_tanpa_jangkar_tidak_menjalankan_apa_pun():
    temuan, jejak = pola_retrieval(store(), "zzz tidak ada")
    assert temuan == []
    assert jejak == []
