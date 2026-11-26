"""Test halaman peta museum (tugas D3).

- Koordinat diambil lewat SPARQL; saringan provinsi ada **di dalam** query.
- Seluruh 28 museum nyata punya koordinat di dalam batas kasar provinsinya
  (menangkap lintang/bujur tertukar atau tanda minus hilang).
- Tanpa JavaScript halaman tetap berisi daftar museum (progressive enhancement).
"""

from __future__ import annotations

import json
import re

import pytest
from fastapi.testclient import TestClient

from main import app, get_store, muat_store
from semweb.peta import kueri_peta, titik_museum
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

sdp:StateMuseum rdfs:subClassOf sdp:Museum .

<https://museumsumatera.id/resource/museum/aceh> a sdp:StateMuseum ;
    sdp:name "Museum Negeri Aceh"@id ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:latitude "5.5483"^^xsd:decimal ;
    sdp:longitude "95.3238"^^xsd:decimal .

<https://museumsumatera.id/resource/museum/medan> a sdp:StateMuseum ;
    sdp:name "Museum Negeri Sumatera Utara"@id ;
    sdp:locatedInProvince res:province-sumut ;
    sdp:latitude "3.5894"^^xsd:decimal ;
    sdp:longitude "98.6747"^^xsd:decimal .

<https://museumsumatera.id/resource/museum/tanpa-koordinat> a sdp:StateMuseum ;
    sdp:name "Museum Tanpa Koordinat"@id ;
    sdp:locatedInProvince res:province-aceh .

res:city-banda-aceh a sdp:City ; sdp:name "Banda Aceh"@id .
res:province-aceh a sdp:Province ; sdp:name "Aceh"@id .
res:province-sumut a sdp:Province ; sdp:name "Sumatera Utara"@id .
"""


@pytest.fixture(scope="module")
def store() -> MuseumStore:
    return MuseumStore.dari_turtle(data=TTL)


# ----------------------------------------------------------------- query


def test_kueri_menulis_prefix_dan_saring_di_sparql():
    q = kueri_peta("Aceh")
    assert "PREFIX sdp:" in q
    assert "FILTER(LCASE(STR(?provinsi)) = LCASE(\"Aceh\"))" in q
    assert "LIMIT" in q


def test_kueri_aman_dari_injeksi():
    q = kueri_peta('Aceh") } DROP ALL #')
    assert 'LCASE("Aceh\\") } DROP ALL #")' in q


def test_titik_semua(store):
    titik = titik_museum(store)
    assert [t["nama"] for t in titik] == [
        "Museum Negeri Aceh",
        "Museum Negeri Sumatera Utara",
        "Museum Tanpa Koordinat",
    ]
    aceh = titik[0]
    assert aceh == {
        "slug": "aceh",
        "nama": "Museum Negeri Aceh",
        "kota": "Banda Aceh",
        "provinsi": "Aceh",
        "lat": pytest.approx(5.5483),
        "lng": pytest.approx(95.3238),
    }
    assert titik[2]["lat"] is None and titik[2]["lng"] is None


def test_saring_provinsi(store):
    assert {t["slug"] for t in titik_museum(store, "aceh")} == {"aceh", "tanpa-koordinat"}
    assert titik_museum(store, "Provinsi Fiktif") == []


# ------------------------------------------------------------ data nyata

# Batas kasar (lintang min, lintang maks, bujur min, bujur maks) per provinsi.
BATAS = {
    "Aceh": (2.0, 6.1, 94.9, 98.3),
    "Sumatera Utara": (0.6, 4.4, 97.0, 100.5),
    "Sumatera Barat": (-3.4, 1.0, 98.5, 101.9),
    "Riau": (-1.2, 2.5, 100.0, 103.9),
    "Kepulauan Riau": (-1.2, 4.8, 103.3, 109.2),
    "Jambi": (-2.8, -0.7, 101.1, 104.6),
    "Sumatera Selatan": (-5.0, -1.6, 102.0, 106.3),
    "Bangka Belitung": (-3.5, -1.4, 105.0, 108.9),
    "Bengkulu": (-5.5, -2.2, 101.0, 104.0),
    "Lampung": (-6.1, -3.7, 103.5, 106.0),
}


@pytest.fixture(scope="module")
def titik_nyata():
    return titik_museum(muat_store())


def test_28_museum_nyata_punya_koordinat(titik_nyata):
    assert len(titik_nyata) == 28
    assert all(t["lat"] is not None and t["lng"] is not None for t in titik_nyata)


def test_koordinat_di_dalam_provinsinya(titik_nyata):
    for t in titik_nyata:
        assert t["provinsi"] in BATAS, t
        lat_min, lat_max, lng_min, lng_max = BATAS[t["provinsi"]]
        assert lat_min <= t["lat"] <= lat_max, f"{t['nama']}: lintang {t['lat']}"
        assert lng_min <= t["lng"] <= lng_max, f"{t['nama']}: bujur {t['lng']}"


# ------------------------------------------------------------------- web


@pytest.fixture()
def client(store):
    app.dependency_overrides[get_store] = lambda: store
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_halaman_peta_tanpa_js_tetap_berisi_daftar(client):
    html = client.get("/peta").text
    # Daftar museum dirender di server, lengkap dengan tautan.
    assert '<a href="/museum/aceh">Museum Negeri Aceh</a>' in html
    assert '<a href="/museum/medan">Museum Negeri Sumatera Utara</a>' in html
    # Peta disembunyikan sampai JavaScript berjalan.
    assert re.search(r'<div id="peta"[^>]*hidden', html)


def test_halaman_peta_menyisipkan_data_json(client):
    html = client.get("/peta").text
    blok = re.search(r'<script type="application/json" id="data-peta">(.*?)</script>', html, re.S)
    data = json.loads(blok.group(1))
    # Museum tanpa koordinat tidak bisa dijadikan penanda.
    assert {d["slug"] for d in data} == {"aceh", "medan"}


def test_leaflet_dari_cdn_dengan_sri(client):
    html = client.get("/peta").text
    assert "unpkg.com/leaflet@1.9.4/dist/leaflet.js" in html
    assert 'integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="' in html
    assert 'integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="' in html


def test_saring_provinsi_tanpa_js(client):
    html = client.get("/peta?provinsi=Sumatera+Utara").text
    assert "Museum Negeri Sumatera Utara" in html
    assert '<a href="/museum/aceh">' not in html
    assert '<option value="Sumatera Utara" selected>' in html


def test_museum_tanpa_koordinat_diberi_keterangan(client):
    html = client.get("/peta").text
    assert "Museum Tanpa Koordinat" in html
    assert "koordinat belum tercatat" in html


def test_navigasi_memuat_peta(client):
    html = client.get("/peta").text
    assert '<a href="/peta" class="aktif" aria-current="page">Peta</a>' in html
