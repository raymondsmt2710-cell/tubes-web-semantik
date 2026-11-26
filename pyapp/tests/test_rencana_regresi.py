"""Test regresi untuk bug yang ditemukan saat menyusun rencana pengembangan.

Test di sini ditulis lebih dulu daripada perbaikannya, sehingga pemilik tugas
mendapat titik mulai yang jelas dan bug tidak kembali diam-diam.
"""

import pytest

from semweb.search import cari_museum, kueri_cari
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://museumsumatera.id/resource/museum/lama> a sdp:Museum ;
    sdp:name "Museum Lama"@id ;
    sdp:establishedYear "950"^^xsd:gYear .

<https://museumsumatera.id/resource/museum/baru> a sdp:Museum ;
    sdp:name "Museum Baru"@id ;
    sdp:establishedYear "1980"^^xsd:gYear .
"""


@pytest.fixture
def store():
    return MuseumStore.dari_turtle(data=TTL)


# --- R1: tahun_min salah untuk tahun < 1000 -------------------------------


def test_tahun_min_1000_tidak_mengembalikan_museum_tahun_950(store):
    """`"950" > "1000"` secara leksikografis, padahal 950 < 1000.

    Perbandingan tahun sebagai string membuat filter tahun minimum salah untuk
    tahun di bawah 1000. Data sekarang semuanya abad ke-19–20 sehingga bug ini
    belum terlihat, tetapi filter yang salah tetap salah. Museum tahun 1980
    memang lolos filter 1000 — yang tidak boleh lolos adalah museum tahun 950.
    """
    hasil = [m["slug"] for m in cari_museum(store, tahun_min=1000)]
    assert "lama" not in hasil, f"museum tahun 950 tidak boleh lolos filter 1000: {hasil}"
    assert hasil == ["baru"]


def test_tahun_min_900_mengembalikan_keduanya(store):
    hasil = {m["slug"] for m in cari_museum(store, tahun_min=900)}
    assert hasil == {"lama", "baru"}


def test_tahun_min_1970_hanya_museum_baru(store):
    hasil = [m["slug"] for m in cari_museum(store, tahun_min=1970)]
    assert hasil == ["baru"]


def test_kueri_tahun_min_tidak_membandingkan_string_mentah():
    """Filter tidak boleh membandingkan `STR(?tahun)` langsung tanpa panjang.

    Ini pemeriksaan bentuk query: perbaikan boleh memakai cara lain, asalkan
    tidak lagi membandingkan string tahun apa adanya.
    """
    q = kueri_cari(tahun_min=1000)
    assert "1000" in q
    # Bila masih membandingkan string, setidaknya harus ada penanganan panjang.
    if 'STR(?tahun) >= "1000"' in q:
        assert "STRLEN" in q or "xsd:integer" in q, (
            "perbandingan string tahun harus memperhitungkan panjang atau "
            "dikonversi ke integer"
        )
