"""R4: `establishedYear` berbentuk tanggal harus tetap tersaring benar.

Bug: `xsd:gYear` bisa berisi bentuk leksikal tidak sah seperti "1915-01-01".
`STR(?tahun)` mengembalikan bentuk leksikal itu (10 karakter), sehingga
perbandingan berbasis panjang pada `kueri_cari` menganggap `STRLEN > 4` selalu
benar dan meloloskan tahun apa pun.

Perbaikan harus di dalam SPARQL, bukan menyaring hasil di Python — aturan modul
ini: semua penyaringan terjadi di query supaya bisa dipindah ke Fuseki apa adanya.
"""

from pathlib import Path

import pytest

from semweb.search import cari_museum
from semweb.store import MuseumStore

AKAR = Path(__file__).resolve().parent.parent.parent
DATA_TTL = AKAR / "data" / "museum-sumatera.ttl"

TTL_TANGGAL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix res: <https://museumsumatera.id/resource/> .

res:museum-tanggal a sdp:Museum ;
    sdp:name "Museum Tanggal"@id ;
    sdp:establishedYear "1915-01-01"^^xsd:gYear .

res:museum-tua a sdp:Museum ;
    sdp:name "Museum Tua"@id ;
    sdp:establishedYear "0950"^^xsd:gYear .

res:museum-baru a sdp:Museum ;
    sdp:name "Museum Baru"@id ;
    sdp:establishedYear "1980"^^xsd:gYear .
"""


def store_tanggal():
    return MuseumStore.dari_turtle(data=TTL_TANGGAL)


def _nama(hasil):
    return sorted(m["nama"] for m in hasil)


def test_tahun_min_menyaring_benar_untuk_data_berbentuk_tanggal():
    """1915 harus lolos ambang 1900 dan gugur pada ambang 1950."""
    assert _nama(cari_museum(store_tanggal(), tahun_min=1900, batas=100)) == [
        "Museum Baru",
        "Museum Tanggal",
    ]
    assert _nama(cari_museum(store_tanggal(), tahun_min=1950, batas=100)) == [
        "Museum Baru"
    ]


def test_tahun_di_bawah_1000_tetap_benar():
    """Regresi R1: "950" tidak boleh dianggap lebih besar dari "1000"."""
    assert _nama(cari_museum(store_tanggal(), tahun_min=1000, batas=100)) == [
        "Museum Baru",
        "Museum Tanggal",
    ]


def test_urut_tahun_membaca_tahun_berbentuk_tanggal():
    """ORDER BY juga harus membaca empat digit pertama, bukan seluruh literal."""
    hasil = cari_museum(store_tanggal(), urut="tahun", batas=100)
    assert [m["tahun"] for m in hasil] == [950, 1915, 1980]


def test_data_asli_tetap_benar():
    """Perbaikan tidak boleh mengubah hasil pada data yang sudah bersih."""
    if not DATA_TTL.exists():
        pytest.skip("data museum tidak ada")
    store = MuseumStore.dari_turtle(path=DATA_TTL)
    assert len(cari_museum(store, tahun_min=1950, batas=1000)) == 11
    assert len(cari_museum(store, tahun_min=1000, batas=1000)) == 13
    assert len(cari_museum(store, batas=1000)) == 28
