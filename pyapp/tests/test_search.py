import pytest

from semweb.search import cari_museum, daftar_era, daftar_provinsi, daftar_tema
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://museumsumatera.id/resource/museum/aceh> a sdp:Museum ;
    sdp:name "Museum Negeri Aceh"@id ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:hasTheme res:theme-etnografi ;
    sdp:hasEra res:era-kolonial ;
    sdp:establishedYear "1915"^^xsd:gYear ;
    sdp:description "Museum tertua di Aceh dengan naskah dan senjata."@id .

<https://museumsumatera.id/resource/museum/tsunami> a sdp:Museum ;
    sdp:name "Museum Tsunami Aceh"@id ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:hasTheme res:theme-sejarah-alam ;
    sdp:hasEra res:era-modern ;
    sdp:establishedYear "2009"^^xsd:gYear ;
    sdp:description "Peringatan bencana tsunami 2004."@id .

<https://museumsumatera.id/resource/museum/sumut> a sdp:Museum ;
    sdp:name "Museum Negeri Sumatera Utara"@id ;
    sdp:locatedInCity res:city-medan ;
    sdp:locatedInProvince res:province-sumut ;
    sdp:hasTheme res:theme-etnografi ;
    sdp:hasEra res:era-modern ;
    sdp:establishedYear "1982"^^xsd:gYear ;
    sdp:description "Koleksi tenun dan arca."@id .

res:city-banda-aceh a sdp:City ; sdp:name "Banda Aceh"@id .
res:city-medan a sdp:City ; sdp:name "Medan"@id .
res:province-aceh a sdp:Province ; sdp:name "Aceh"@id .
res:province-sumut a sdp:Province ; sdp:name "Sumatera Utara"@id .
res:theme-etnografi a sdp:Theme ; sdp:name "Etnografi"@id .
res:theme-sejarah-alam a sdp:Theme ; sdp:name "Sejarah Alam"@id .
res:era-kolonial a sdp:Era ; sdp:name "Kolonial"@id .
res:era-modern a sdp:Era ; sdp:name "Modern"@id .
"""


@pytest.fixture
def store():
    return MuseumStore.dari_turtle(data=TTL)


def test_tanpa_filter_mengembalikan_semua(store):
    assert len(cari_museum(store)) == 3


def test_kata_kunci_mencocokkan_nama(store):
    hasil = cari_museum(store, q="tsunami")
    assert [m["slug"] for m in hasil] == ["tsunami"]


def test_kata_kunci_mencocokkan_deskripsi(store):
    hasil = cari_museum(store, q="tenun")
    assert [m["slug"] for m in hasil] == ["sumut"]


def test_kata_kunci_banyak_kata_harus_semuanya_cocok(store):
    assert len(cari_museum(store, q="museum aceh")) == 2
    assert len(cari_museum(store, q="museum aceh tenun")) == 0


def test_filter_provinsi(store):
    hasil = cari_museum(store, provinsi="Aceh")
    assert {m["slug"] for m in hasil} == {"aceh", "tsunami"}


def test_filter_tema(store):
    hasil = cari_museum(store, tema="Etnografi")
    assert {m["slug"] for m in hasil} == {"aceh", "sumut"}


def test_filter_tahun_minimum(store):
    hasil = cari_museum(store, tahun_min=1980)
    assert {m["slug"] for m in hasil} == {"tsunami", "sumut"}


def test_filter_gabungan(store):
    hasil = cari_museum(store, provinsi="Aceh", tahun_min=2000)
    assert [m["slug"] for m in hasil] == ["tsunami"]


def test_urut_nama_dan_tahun(store):
    nama = [m["slug"] for m in cari_museum(store, urut="nama")]
    assert nama == sorted(nama)
    tahun = [m["tahun"] for m in cari_museum(store, urut="tahun")]
    assert tahun == sorted(tahun)


def test_batas_dihormati(store):
    assert len(cari_museum(store, batas=2)) == 2


def test_hasil_memuat_bidang_yang_dibutuhkan_ui(store):
    m = cari_museum(store, q="tsunami")[0]
    for kunci in ("slug", "nama", "kota", "provinsi", "tema", "era", "tahun", "deskripsi"):
        assert kunci in m


def test_daftar_provinsi_unik_dan_terurut(store):
    assert daftar_provinsi(store) == ["Aceh", "Sumatera Utara"]


def test_daftar_tema_unik_dan_terurut(store):
    assert daftar_tema(store) == ["Etnografi", "Sejarah Alam"]


def test_daftar_era_unik_dan_terurut(store):
    assert daftar_era(store) == ["Kolonial", "Modern"]


def test_query_selalu_memuat_prefix_lengkap(store):
    """Aturan materi P10: PREFIX ditulis lengkap, bukan disuntikkan editor."""
    from semweb.search import kueri_cari

    q = kueri_cari(q="aceh", batas=10)
    for p in ("PREFIX sdp:", "PREFIX res:", "PREFIX rdfs:", "PREFIX xsd:"):
        assert p in q


def test_kata_kunci_tidak_bisa_menyuntikkan_sparql(store):
    hasil = cari_museum(store, q='" . } UNION { ?s ?p ?o')
    assert hasil == []


def test_museum_tanpa_tahun_tidak_menggagalkan_urut_tahun(store):
    """Data nyata punya museum tanpa establishedYear — harus tetap tampil."""
    ttl = (
        '@prefix sdp: <https://museumsumatera.id/ontology#> .\n'
        "@prefix res: <https://museumsumatera.id/resource/> .\n"
        '<https://museumsumatera.id/resource/museum/x> a sdp:Museum ;\n'
        '    sdp:name "Museum Tanpa Tahun"@id .\n'
    )
    s = MuseumStore.dari_turtle(data=ttl)
    hasil = cari_museum(s, urut="tahun")
    assert len(hasil) == 1
    assert hasil[0]["tahun"] is None
