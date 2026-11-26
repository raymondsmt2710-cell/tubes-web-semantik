"""Test aplikasi web: halaman dan API JSON.

Store disuntikkan lewat dependency override supaya test tidak bergantung pada
berkas data di disk; test ini memeriksa perilaku route, bukan isi data nyata.
"""

import pytest
from fastapi.testclient import TestClient

from main import app, get_store
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://museumsumatera.id/resource/museum/aceh> a sdp:Museum, sdp:StateMuseum ;
    sdp:name "Museum Negeri Aceh"@id ;
    sdp:description "Museum tertua di Aceh."@id ;
    sdp:address "Jl. Sultan Mahmudsyah"@id ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:hasTheme res:theme-etnografi ;
    sdp:hasEra res:era-kolonial ;
    sdp:establishedYear "1915"^^xsd:gYear ;
    sdp:hasExhibit res:museum-aceh-exhibit-1 ;
    sdp:hasImage res:museum-aceh-image-1 ;
    sdp:hasSource res:museum-aceh-source-1 .

res:museum-aceh-exhibit-1 a sdp:Exhibit ;
    sdp:exhibitIndex 1 ;
    sdp:exhibitTitle "Lonceng Cakra Donya"@id ;
    sdp:exhibitDescription "Lonceng perunggu dari Kesultanan Pasai."@id ;
    sdp:exhibitPeriod "abad ke-15"@id ;
    sdp:exhibitOrigin "Pasai"@id ;
    sdp:exhibitMaterial "perunggu"@id ;
    sdp:exhibitHighlight true .

res:museum-aceh-image-1 a sdp:Image ;
    sdp:imageIndex 1 ;
    sdp:imageUrl "/images/museums/museum-negeri-aceh/1.jpg"^^xsd:anyURI ;
    sdp:imageTitle "Gedung pameran tetap"@id ;
    sdp:imageCredit "Si Gam"@id ;
    sdp:imageLicense "CC BY-SA 3.0"@id ;
    sdp:imageSource "https://commons.wikimedia.org/wiki/File:X.jpg"^^xsd:anyURI ;
    sdp:imageDetail res:museum-aceh-image-1-detail-1 .

res:museum-aceh-image-1-detail-1 a sdp:ImageDetail ;
    sdp:detailIndex 1 ;
    sdp:detailText "Bentuk atap meniru rumah tradisional Aceh."@id .

res:museum-aceh-source-1 a sdp:Source ;
    sdp:sourceIndex 1 ;
    sdp:sourceLabel "Wikipedia"@id ;
    sdp:sourceUrl "https://id.wikipedia.org/wiki/Museum_Aceh"^^xsd:anyURI .

res:city-banda-aceh a sdp:City ; sdp:name "Banda Aceh"@id .
res:province-aceh a sdp:Province ; sdp:name "Aceh"@id .
res:theme-etnografi a sdp:Theme ; sdp:name "Etnografi"@id .
res:era-kolonial a sdp:Era ; sdp:name "Kolonial"@id .

sdp:locatedInProvince a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Province .
"""


@pytest.fixture
def client():
    store = MuseumStore.dari_turtle(data=TTL)
    app.dependency_overrides[get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()


# --- halaman --------------------------------------------------------------


def test_halaman_depan_200(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Museum" in r.text


def test_cari_menampilkan_hasil(client):
    r = client.get("/cari", params={"q": "aceh"})
    assert r.status_code == 200
    assert "Museum Negeri Aceh" in r.text


def test_cari_tanpa_hasil_memberi_pesan_bukan_error(client):
    r = client.get("/cari", params={"q": "zzzTidakAda"})
    assert r.status_code == 200
    assert "tidak ditemukan" in r.text.lower()


def test_museum_tidak_dikenal_404(client):
    assert client.get("/museum/tidak-ada").status_code == 404


@pytest.mark.parametrize(
    "slug",
    [
        "'; DROP",
        "museum/'; DROP",
        "../../etc/passwd",
        "museum aceh",
        "Museum-Negeri-Aceh",
        "a" * 200,
        "<script>",
        "museum%00",
    ],
)
def test_slug_tidak_sah_ditolak_tanpa_membentuk_iri(client, slug):
    """Slug dari URL tidak boleh masuk ke `URIRef` mentah.

    Tanpa validasi, rdflib memperingatkan "does not look like a valid URI" dan
    IRI sampah ikut dibuat — jalur yang tidak perlu ada untuk data yang slug-nya
    selalu huruf kecil dan tanda hubung.
    """
    assert client.get(f"/museum/{slug}").status_code == 404
    assert client.get(f"/api/museum/{slug}").status_code == 404


def test_slug_sah_tetap_diterima(client):
    assert client.get("/museum/aceh").status_code == 200


def test_halaman_museum_menampilkan_isi_pameran_dan_galeri(client):
    r = client.get("/museum/aceh")
    assert r.status_code == 200
    assert "Isi pameran" in r.text
    assert "Galeri" in r.text
    assert "Lonceng Cakra Donya" in r.text


def test_halaman_museum_menampilkan_metadata_pameran(client):
    r = client.get("/museum/aceh")
    assert "abad ke-15" in r.text
    assert "perunggu" in r.text


def test_halaman_museum_menampilkan_poin_galeri(client):
    r = client.get("/museum/aceh")
    assert "Bentuk atap meniru rumah tradisional Aceh." in r.text


def test_halaman_museum_tidak_menampilkan_none(client):
    """Data nyata punya banyak bidang null; jangan pernah tampilkan "None"."""
    r = client.get("/museum/aceh")
    assert "None" not in r.text


def test_tanya_menampilkan_query_dan_guard(client):
    r = client.get("/tanya", params={"q": "pameran apa saja di Museum Negeri Aceh?"})
    assert r.status_code == 200
    assert "SELECT" in r.text
    assert "guard" in r.text.lower()


def test_tanya_pertanyaan_luar_domain_memberi_pesan_jelas(client):
    r = client.get("/tanya", params={"q": "berapa harga tiket pesawat?"})
    assert r.status_code == 200
    assert "tidak menyebut" in r.text.lower()


def test_metode_menampilkan_perbandingan_inferensi(client):
    r = client.get("/metode")
    assert r.status_code == 200
    assert "asserted" in r.text.lower()


# --- API JSON -------------------------------------------------------------


def test_api_cari_mengembalikan_json(client):
    r = client.get("/api/cari", params={"q": "aceh"})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data["museum"], list)
    assert data["museum"][0]["nama"] == "Museum Negeri Aceh"


def test_api_museum_mengembalikan_detail(client):
    r = client.get("/api/museum/aceh")
    assert r.status_code == 200
    data = r.json()
    assert data["museum"]["nama"] == "Museum Negeri Aceh"
    assert data["museum"]["exhibits"][0]["judul"] == "Lonceng Cakra Donya"


def test_api_museum_tidak_ada_404(client):
    assert client.get("/api/museum/tidak-ada").status_code == 404


def test_api_tanya_mengembalikan_query_guard_dan_jawaban(client):
    r = client.get("/api/tanya", params={"q": "pameran apa saja di Museum Negeri Aceh?"})
    assert r.status_code == 200
    data = r.json()
    for kunci in ("pertanyaan", "query", "lolos", "jawaban", "pesan"):
        assert kunci in data


def test_api_metode_mengembalikan_angka_penalaran(client):
    r = client.get("/api/metode")
    assert r.status_code == 200
    data = r.json()
    assert data["perbandingan"]["asserted"] > 0
    assert data["perbandingan"]["inferred"] >= 0


def test_api_tidak_melempar_500_untuk_input_aneh(client):
    for q in ['" . } UNION { ?s ?p ?o', "'; DROP TABLE", "<script>alert(1)</script>", ""]:
        r = client.get("/api/cari", params={"q": q})
        assert r.status_code == 200, q
