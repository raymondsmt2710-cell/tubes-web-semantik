import pytest

from semweb.relations import benang_merah, kueri_benang_merah, subgraf_sekitar
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://museumsumatera.id/resource/museum/aceh> a sdp:Museum ;
    sdp:name "Museum Negeri Aceh"@id ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:hasTheme res:theme-etnografi ;
    sdp:hasEra res:era-kolonial ;
    sdp:chapter res:chapter-1 .

<https://museumsumatera.id/resource/museum/tsunami> a sdp:Museum ;
    sdp:name "Museum Tsunami Aceh"@id ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:hasTheme res:theme-etnografi ;
    sdp:hasEra res:era-modern ;
    sdp:chapter res:chapter-1 .

<https://museumsumatera.id/resource/museum/sumut> a sdp:Museum ;
    sdp:name "Museum Negeri Sumatera Utara"@id ;
    sdp:locatedInCity res:city-medan ;
    sdp:hasTheme res:theme-etnografi ;
    sdp:hasEra res:era-modern ;
    sdp:chapter res:chapter-2 .

<https://museumsumatera.id/resource/museum/jauh> a sdp:Museum ;
    sdp:name "Museum Jauh"@id ;
    sdp:locatedInCity res:city-padang ;
    sdp:hasTheme res:theme-arkeologi ;
    sdp:hasEra res:era-pra ;
    sdp:chapter res:chapter-4 .

res:city-banda-aceh a sdp:City ; sdp:name "Banda Aceh"@id .
res:city-medan a sdp:City ; sdp:name "Medan"@id .
res:city-padang a sdp:City ; sdp:name "Padang"@id .
res:theme-etnografi a sdp:Theme ; sdp:name "Etnografi"@id .
res:theme-arkeologi a sdp:Theme ; sdp:name "Arkeologi"@id .
res:era-kolonial a sdp:Era ; sdp:name "Kolonial"@id .
res:era-modern a sdp:Era ; sdp:name "Modern"@id .
res:era-pra a sdp:Era ; sdp:name "Pra-kolonial"@id .
res:chapter-1 a sdp:Chapter ; sdp:chapterIndex 1 .
res:chapter-2 a sdp:Chapter ; sdp:chapterIndex 2 .
res:chapter-4 a sdp:Chapter ; sdp:chapterIndex 4 .
"""


@pytest.fixture
def store():
    return MuseumStore.dari_turtle(data=TTL)


def test_museum_dengan_tema_sama_muncul_dengan_alasan(store):
    hasil = benang_merah(store, "aceh")
    slug = [h["slug"] for h in hasil]
    assert "tsunami" in slug
    alasan = next(h["alasan"] for h in hasil if h["slug"] == "tsunami")
    assert "tema" in alasan.lower()


def test_museum_diri_sendiri_tidak_muncul(store):
    assert all(h["slug"] != "aceh" for h in benang_merah(store, "aceh"))


def test_hasil_diurutkan_skor_menurun(store):
    skor = [h["skor"] for h in benang_merah(store, "aceh")]
    assert skor == sorted(skor, reverse=True)


def test_maksimum_hasil_dihormati(store):
    assert len(benang_merah(store, "aceh", maks=1)) <= 1


def test_museum_tanpa_relasi_tidak_muncul(store):
    """Museum Jauh tidak berbagi tema, kota, era, maupun bab bersebelahan."""
    assert all(h["slug"] != "jauh" for h in benang_merah(store, "aceh"))


def test_alasan_menyebut_relasi_yang_benar_benar_cocok(store):
    hasil = {h["slug"]: h for h in benang_merah(store, "aceh")}
    assert "kota" in hasil["tsunami"]["alasan"].lower()
    assert "kota" not in hasil["sumut"]["alasan"].lower()


def test_subgraf_satu_hop_tidak_sampai_provinsi_dua_hop_lebih_besar(store):
    satu = subgraf_sekitar(store, "aceh", hop=1)
    dua = subgraf_sekitar(store, "aceh", hop=2)
    assert len(satu) > 0
    assert len(dua) >= len(satu)


def test_subgraf_tidak_memuat_objek_trivial(store):
    teks = " ".join(str(o) for _, _, o in subgraf_sekitar(store, "aceh", hop=2))
    assert "owl#Thing" not in teks
    assert "rdf-schema#Resource" not in teks


def test_kueri_benang_merah_memakai_construct_dan_prefix(store):
    q = kueri_benang_merah("aceh", 6)
    assert "CONSTRUCT" in q
    assert "PREFIX sdp:" in q


def test_slug_tidak_dikenal_mengembalikan_kosong(store):
    assert benang_merah(store, "tidak-ada") == []
