"""Test perluasan cakupan pertanyaan (C4).

Lima kandidat dari dokumen tugas, masing-masing harus dikenali dengan benar:

1. "museum apa saja yang punya foto?"       -> museum dengan `hasImage`
2. "museum yang berdiri sebelum 1950?"      -> filter tahun
3. "apa hubungan Museum A dengan Museum B?" -> `relatedMuseum`
4. "museum tertua di Aceh?"                 -> urut tahun, dalam wilayah
5. "tema apa saja yang ada?"                -> daftar tema, bukan hitung

Yang dijaga bersamaan: pelonggaran ini **tidak boleh** membuat pertanyaan di
luar domain lolos. "harga tiket pesawat" harus tetap ditolak.
"""

from __future__ import annotations

import pytest

from semweb.nl2sparql import aman, intent, jawab, ke_sparql
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://museumsumatera.id/resource/museum/negeri-aceh> a sdp:Museum ;
    sdp:name "Museum Negeri Aceh"@id ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:hasTheme res:theme-etnografi ;
    sdp:establishedYear "1915"^^xsd:gYear ;
    sdp:hasImage res:aceh-img-1 ;
    sdp:hasExhibit res:aceh-ex-1 , res:aceh-ex-2 ;
    sdp:relatedMuseum <https://museumsumatera.id/resource/museum/tsunami-aceh> .

<https://museumsumatera.id/resource/museum/tsunami-aceh> a sdp:Museum ;
    sdp:name "Museum Tsunami Aceh"@id ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:establishedYear "2009"^^xsd:gYear ;
    sdp:hasImage res:tsunami-img-1 .

res:aceh-ex-1 a sdp:Exhibit ; sdp:exhibitTitle "Lonceng Cakra Donya"@id .
res:aceh-ex-2 a sdp:Exhibit ; sdp:exhibitTitle "Rumoh Aceh"@id .

res:city-banda-aceh a sdp:City ;
    sdp:name "Banda Aceh"@id ;
    sdp:partOfProvince res:province-aceh .

<https://museumsumatera.id/resource/museum/tua-sumut> a sdp:Museum ;
    sdp:name "Museum Tua Sumatera Utara"@id ;
    sdp:locatedInProvince res:province-sumut ;
    sdp:establishedYear "1900"^^xsd:gYear .

res:aceh-img-1 a sdp:Image ; sdp:imageTitle "Foto Aceh"@id .
res:tsunami-img-1 a sdp:Image ; sdp:imageTitle "Foto Tsunami"@id .

res:province-aceh a sdp:Province ; sdp:name "Aceh"@id .
res:province-sumut a sdp:Province ; sdp:name "Sumatera Utara"@id .
res:theme-etnografi a sdp:Theme ; sdp:name "Etnografi"@id .
res:theme-sejarah a sdp:Theme ; sdp:name "Sejarah"@id .

sdp:locatedInProvince a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Province .
sdp:locatedInCity a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:City .
sdp:partOfProvince a owl:ObjectProperty ;
    rdfs:domain sdp:City ; rdfs:range sdp:Province .
sdp:hasExhibit a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Exhibit .
sdp:exhibitTitle a owl:DatatypeProperty ;
    rdfs:domain sdp:Exhibit ; rdfs:range xsd:string .
sdp:hasTheme a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Theme .
sdp:hasImage a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Image .
sdp:relatedMuseum a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Museum .
sdp:name a owl:DatatypeProperty ;
    rdfs:domain sdp:Museum ; rdfs:range xsd:string .
sdp:imageTitle a owl:DatatypeProperty ;
    rdfs:domain sdp:Image ; rdfs:range xsd:string .
sdp:establishedYear a owl:DatatypeProperty ;
    rdfs:domain sdp:Museum ; rdfs:range xsd:gYear .
"""


@pytest.fixture
def store():
    return MuseumStore.dari_turtle(data=TTL)


# ============================================ 1. museum yang punya foto


def test_punya_foto_dikenali_sebagai_daftar_galeri(store):
    niat = intent("museum apa saja yang punya foto?", store)
    assert niat.jenis == "punya_foto"
    assert niat.topik == "museum"


def test_punya_foto_menghasilkan_query_yang_lolos_guard(store):
    q = ke_sparql("museum apa saja yang punya foto?", store)
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_punya_foto_hanya_mengembalikan_museum_yang_punya_foto(store):
    hasil = jawab("museum apa saja yang punya foto?", store)
    assert hasil.lolos is True
    assert "Museum Tua Sumatera Utara" not in hasil.jawaban


def test_punya_foto_tidak_menghasilkan_duplikat(store):
    """Museum dengan tiga foto tidak boleh muncul tiga kali.

    Tanpa GROUP BY, satu museum menghabiskan beberapa baris LIMIT dan pengguna
    melihat daftar yang penuh nama berulang — bukan daftar museum.
    """
    hasil = jawab("museum apa saja yang punya foto?", store)
    museum = [r[0] for r in hasil.baris if r]
    assert len(museum) == len(set(museum)), f"ada duplikat: {museum}"


def test_punya_foto_tidak_menghitung(store):
    niat = intent("museum apa saja yang punya foto?", store)
    assert niat.jenis != "hitung"


# ============================================ 2. berdiri sebelum tahun


def test_sebelum_tahun_dikenali(store):
    niat = intent("museum yang berdiri sebelum 1950?", store)
    assert niat.jenis == "batas_tahun"
    assert niat.topik == "museum"
    assert niat.atribut == "bawah:1950"


def test_sebelum_tahun_query_lolos_guard(store):
    q = ke_sparql("museum yang berdiri sebelum 1950?", store)
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_sebelum_tahun_memakai_filter_tahun(store):
    q = ke_sparql("museum yang berdiri sebelum 1950?", store)
    assert "establishedYear" in q
    assert "1950" in q


def test_sebelum_tahun_menyaring_dengan_benar(store):
    hasil = jawab("museum yang berdiri sebelum 1950?", store)
    assert hasil.lolos is True
    assert "Museum Negeri Aceh" in hasil.jawaban
    assert "Museum Tua Sumatera Utara" in hasil.jawaban
    assert "Museum Tsunami Aceh" not in hasil.jawaban


def test_sesudah_tahun_juga_dikenali(store):
    hasil = jawab("museum yang berdiri setelah 2000?", store)
    assert hasil.lolos is True
    assert "Museum Tsunami Aceh" in hasil.jawaban
    assert "Museum Tua Sumatera Utara" not in hasil.jawaban


# ============================================ 3. hubungan dua museum


def test_hubungan_dua_museum_dikenali(store):
    niat = intent("apa hubungan Museum Negeri Aceh dengan Museum Tsunami Aceh?", store)
    assert niat.jenis != "tidak_dikenal"


def test_hubungan_dua_museum_query_lolos_guard(store):
    q = ke_sparql("apa hubungan Museum Negeri Aceh dengan Museum Tsunami Aceh?", store)
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_hubungan_dua_museum_menyebut_keduanya(store):
    hasil = jawab("apa hubungan Museum Negeri Aceh dengan Museum Tsunami Aceh?", store)
    assert hasil.lolos is True
    assert hasil.jawaban
    assert "Tidak ditemukan" not in hasil.jawaban
    assert hasil.baris, "hubungan harus menghasilkan minimal satu baris"


def test_hubungan_menemukan_provinsi_yang_sama(store):
    hasil = jawab("apa hubungan Museum Negeri Aceh dengan Museum Tsunami Aceh?", store)
    assert "province-aceh" in hasil.jawaban


# ============================================ 4. museum tertua


def test_tertua_dikenali(store):
    niat = intent("museum tertua di Aceh?", store)
    assert niat.jenis == "urut_tahun"
    assert niat.atribut == "naik"


def test_tertua_query_lolos_guard(store):
    q = ke_sparql("museum tertua di Aceh?", store)
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_tertua_mengurutkan_tahun_naik(store):
    q = ke_sparql("museum tertua di Aceh?", store)
    assert "ORDER BY" in q
    assert "establishedYear" in q


def test_tertua_mengembalikan_yang_paling_tua(store):
    hasil = jawab("museum tertua di Aceh?", store)
    assert hasil.lolos is True
    assert "Museum Negeri Aceh" in hasil.jawaban


def test_tertua_mengembalikan_satu_museum_saja(store):
    """"Museum tertua" menanyakan satu museum, bukan daftar semua museum."""
    hasil = jawab("museum tertua di Aceh?", store)
    assert len(hasil.baris) == 1, f"dapat {len(hasil.baris)} baris"
    assert "tertua" in hasil.jawaban.lower()


def test_tertua_tidak_memuat_museum_yang_lebih_muda(store):
    hasil = jawab("museum tertua di Aceh?", store)
    assert "Museum Tsunami Aceh" not in hasil.jawaban


def test_termuda_mengembalikan_yang_paling_baru(store):
    hasil = jawab("museum termuda di Aceh?", store)
    assert hasil.lolos is True
    assert "Museum Tsunami Aceh" in hasil.jawaban
    assert "termuda" in hasil.jawaban.lower()


# ============================================ 5. daftar tema


def test_daftar_tema_dikenali(store):
    niat = intent("tema apa saja yang ada?", store)
    assert niat.jenis == "daftar"
    assert niat.topik == "tema"


def test_daftar_tema_bukan_hitung(store):
    niat = intent("tema apa saja yang ada?", store)
    assert niat.jenis != "hitung"


def test_daftar_tema_query_lolos_guard(store):
    q = ke_sparql("tema apa saja yang ada?", store)
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_daftar_tema_mengembalikan_nama_tema(store):
    hasil = jawab("tema apa saja yang ada?", store)
    assert hasil.lolos is True
    assert "Etnografi" in hasil.jawaban or "Sejarah" in hasil.jawaban


def test_daftar_tema_tidak_menyebut_museum(store):
    """Kalimat pertama tidak boleh berbunyi 'Ditemukan N museum'."""
    hasil = jawab("tema apa saja yang ada?", store)
    kalimat = hasil.jawaban.split("\n")[0]
    assert "tema" in kalimat.lower()
    assert "museum" not in kalimat.lower()


# ============================ topik museum vs kata wilayah


def test_museum_di_kota_tetap_bertopik_museum(store):
    """'museum apa saja di kota X' menanyakan museum, bukan daftar kota.

    Kata "kota" muncul, tetapi hanya sebagai penyaring wilayah. Sebelum
    diperbaiki, jawabannya berbunyi "Ditemukan N kota" padahal isinya nama
    museum.
    """
    hasil = jawab("museum apa saja di kota Banda Aceh?", store)
    assert hasil.lolos is True
    kalimat = hasil.jawaban.split("\n")[0]
    assert "museum" in kalimat.lower()
    assert "Museum Negeri Aceh" in kalimat


def test_hitung_museum_di_kota_menghitung_museum(store):
    hasil = jawab("berapa museum di kota Banda Aceh?", store)
    assert hasil.lolos is True
    assert "museum" in hasil.jawaban.lower()


def test_museum_di_provinsi_tetap_bertopik_museum(store):
    hasil = jawab("museum apa saja di provinsi Aceh?", store)
    kalimat = hasil.jawaban.split("\n")[0]
    assert "museum" in kalimat.lower()


def test_berapa_pameran_tidak_berubah_jadi_museum(store):
    """Perbaikan topik tidak boleh menimpa topik yang lebih spesifik."""
    hasil = jawab("berapa pameran di Museum Negeri Aceh?", store)
    assert "pameran" in hasil.jawaban.lower()


def test_berapa_foto_tidak_berubah_jadi_museum(store):
    hasil = jawab("berapa foto di Museum Negeri Aceh?", store)
    assert "foto" in hasil.jawaban.lower()


def test_daftar_pameran_tidak_berubah_jadi_museum(store):
    hasil = jawab("apa saja pameran di Museum Negeri Aceh?", store)
    assert hasil.lolos is True
    assert "pameran" in hasil.jawaban.lower()


# ============================================ jangan merusak yang lama


@pytest.mark.parametrize(
    "pertanyaan",
    [
        "berapa harga tiket pesawat ke Aceh?",
        "jam buka museum?",
        "berapa biaya parkir?",
        "presiden pertama Indonesia siapa?",
        "cuaca di Medan hari ini?",
    ],
)
def test_pertanyaan_luar_domain_tetap_ditolak(store, pertanyaan):
    niat = intent(pertanyaan, store)
    assert niat.jenis == "tidak_dikenal", f"{pertanyaan} -> {niat.jenis}"


def test_berapa_museum_tetap_hitung(store):
    niat = intent("ada berapa museum?", store)
    assert niat.jenis == "hitung"


def test_berapa_pameran_tetap_hitung(store):
    niat = intent("berapa pameran di Museum Negeri Aceh?", store)
    assert niat.jenis == "hitung"


def test_kapan_berdiri_tetap_atribut(store):
    niat = intent("kapan Museum Negeri Aceh berdiri?", store)
    assert niat.jenis == "atribut"
    assert niat.atribut == "establishedYear"


def test_daftar_museum_biasa_tetap_jalan(store):
    hasil = jawab("museum apa saja di Aceh?", store)
    assert hasil.lolos is True
    assert "Museum Negeri Aceh" in hasil.jawaban
