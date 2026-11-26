"""Test perbaikan jangkar untuk nama museum yang disebut sebagian.

Bug yang dikunci: pertanyaan "Museum Aceh" menghasilkan jangkar **provinsi
Aceh**, bukan museum "Museum Negeri Aceh", karena pencocokan menuntut label
lengkap muncul di teks. Akibatnya jawaban menunjuk provinsi, bukan museum.

Yang dijaga bersamaan:

- Perbaikan ini tidak boleh merusak kasus yang sudah benar.
  "berapa pameran di Museum Tsunami Aceh?" harus tetap menjawab 4, bukan
  seluruh pameran di graf.
- Pertanyaan yang benar-benar menyebut dua museum harus mengembalikan keduanya.
- Pertanyaan asing tetap tidak menghasilkan jangkar.
"""

from __future__ import annotations

import pytest

from semweb.graphrag import jangkar
from semweb.nl2sparql import jawab
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
    sdp:hasExhibit res:aceh-ex-1 , res:aceh-ex-2 .

<https://museumsumatera.id/resource/museum/tsunami-aceh> a sdp:Museum ;
    sdp:name "Museum Tsunami Aceh"@id ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:hasExhibit res:tsunami-ex-1 , res:tsunami-ex-2 , res:tsunami-ex-3 , res:tsunami-ex-4 .

<https://museumsumatera.id/resource/museum/negeri-sumatera-utara> a sdp:Museum ;
    sdp:name "Museum Negeri Sumatera Utara"@id ;
    sdp:locatedInProvince res:province-sumut .

res:aceh-ex-1 a sdp:Exhibit ; sdp:exhibitTitle "Lonceng Cakra Donya"@id .
res:aceh-ex-2 a sdp:Exhibit ; sdp:exhibitTitle "Kain Aceh"@id .
res:tsunami-ex-1 a sdp:Exhibit ; sdp:exhibitTitle "Rumah Aceh"@id .
res:tsunami-ex-2 a sdp:Exhibit ; sdp:exhibitTitle "Foto Tsunami"@id .
res:tsunami-ex-3 a sdp:Exhibit ; sdp:exhibitTitle "Jam Berhenti"@id .
res:tsunami-ex-4 a sdp:Exhibit ; sdp:exhibitTitle "Kapal Apung"@id .

res:province-aceh a sdp:Province ; sdp:name "Aceh"@id .
res:province-sumut a sdp:Province ; sdp:name "Sumatera Utara"@id .

res:city-banda-aceh a sdp:City ;
    sdp:name "Banda Aceh"@id ;
    sdp:partOfProvince res:province-aceh .

sdp:locatedInProvince a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Province .
sdp:hasExhibit a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Exhibit .
sdp:name a owl:DatatypeProperty ;
    rdfs:domain sdp:Museum ; rdfs:range xsd:string .
sdp:exhibitTitle a owl:DatatypeProperty ;
    rdfs:domain sdp:Exhibit ; rdfs:range xsd:string .
"""


@pytest.fixture
def store():
    return MuseumStore.dari_turtle(data=TTL)


def _museum_pertama(daftar):
    for j in daftar:
        if j.jenis == "museum":
            return j
    return None


# ------------------------------------------------------- kasus bug utama


def test_museum_aceh_mengarah_ke_museum_bukan_provinsi(store):
    """'Museum Aceh' ambigu: dua museum memuat kata 'aceh'.

    Yang dikunci bukan pilihan salah satunya, melainkan bahwa museum **ikut**
    dipertimbangkan. Sebelum perbaikan, hasilnya hanya provinsi.
    """
    hasil = jangkar(store, "Museum Aceh")
    label_museum = {j.label for j in hasil if j.jenis == "museum"}
    assert label_museum, f"tidak ada museum pada {[(j.jenis, j.label) for j in hasil]}"
    assert "Museum Negeri Aceh" in label_museum


def test_museum_aceh_tidak_menjadikan_provinsi_sebagai_jangkar_utama(store):
    hasil = jangkar(store, "Museum Aceh")
    assert hasil[0].jenis == "museum"


def test_museum_tsunami_aceh_tetap_memilih_label_terpanjang(store):
    hasil = jangkar(store, "Museum Tsunami Aceh")
    assert hasil[0].label == "Museum Tsunami Aceh"


def test_museum_negeri_aceh_lengkap_tetap_benar(store):
    hasil = jangkar(store, "Museum Negeri Aceh")
    assert hasil[0].label == "Museum Negeri Aceh"


# ------------------------------------------------------- dua museum sekaligus


def test_dua_museum_disebut_mengembalikan_keduanya(store):
    hasil = jangkar(store, "Bandingkan Museum Tsunami Aceh dengan Museum Negeri Aceh")
    label = {j.label for j in hasil if j.jenis == "museum"}
    assert "Museum Tsunami Aceh" in label
    assert "Museum Negeri Aceh" in label


# ------------------------------------------------------- jangan merusak yang benar


def test_pameran_museum_tsunami_tetap_empat(store):
    hasil = jawab("berapa pameran di Museum Tsunami Aceh?", store)
    assert hasil.lolos is True
    assert "4" in hasil.jawaban, hasil.jawaban


def test_pameran_museum_negeri_aceh_tetap_dua(store):
    hasil = jawab("berapa pameran di Museum Negeri Aceh?", store)
    assert hasil.lolos is True
    assert "2" in hasil.jawaban, hasil.jawaban


def test_pertanyaan_asing_tetap_tanpa_jangkar(store):
    assert jangkar(store, "berapa harga tiket pesawat") == []


def test_provinsi_tetap_ditemukan_saat_hanya_provinsi_disebut(store):
    hasil = jangkar(store, "museum apa saja di Aceh")
    assert hasil[0].jenis == "provinsi"
    assert hasil[0].label == "Aceh"


def test_penyaringan_wilayah_tidak_berubah_jadi_jangkar_museum(store):
    """'museum di Aceh' menyaring wilayah, bukan menamai museum.

    Tanpa penjagaan ini, jalur pencocokan sebagian akan memilih dua museum yang
    kebetulan berbagi kata "aceh", dan pertanyaan yang seharusnya dijawab
    "museum di provinsi Aceh" berubah menjadi "museum tertentu".
    """
    hasil = jangkar(store, "museum di Aceh")
    assert hasil[0].jenis == "provinsi"
    assert not any(j.jenis == "museum" for j in hasil)


def test_kota_ditemukan_saat_menyebut_nama_kota(store):
    hasil = jangkar(store, "museum di kota Banda Aceh")
    assert hasil[0].jenis == "kota"


# ------------------------------------------------------- batas & bentuk


def test_batas_maks_dihormati(store):
    hasil = jangkar(store, "Museum Tsunami Aceh dan Museum Negeri Aceh dan Aceh", maks=2)
    assert len(hasil) <= 2


def test_hasil_jangkar_selalu_berisi_iri_dan_jenis(store):
    for j in jangkar(store, "Museum Tsunami Aceh"):
        assert str(j.iri).startswith("https://museumsumatera.id/resource/")
        assert j.jenis in ("museum", "kota", "provinsi", "tema", "era")
