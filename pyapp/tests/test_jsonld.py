"""Test JSON-LD schema.org (tugas D1, materi P3).

Yang dijaga:

1. JSON-LD bila di-parse balik ke RDF menghasilkan nilai yang **sama** dengan
   graf asal untuk setiap properti yang dipetakan (round-trip).
2. Tidak ada ``None`` / ``null`` yang bocor ke dokumen.
3. Halaman museum menyisipkan ``<script type="application/ld+json">`` yang sah,
   dan endpoint ``/api/museum/{slug}.jsonld`` menyajikan dokumen yang sama.
"""

from __future__ import annotations

import json
import re
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from rdflib import Literal, URIRef
from rdflib.namespace import RDF

from main import app, get_store, muat_store
from semweb.jsonld import SCHEMA, ke_graf, museum_jsonld, semua_museum_jsonld
from semweb.namespace import SDP
from semweb.store import MuseumStore

BASIS = "https://contoh.test/"
IRI = URIRef("https://museumsumatera.id/resource/museum/aceh")

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

sdp:StateMuseum rdfs:subClassOf sdp:Museum .

<https://museumsumatera.id/resource/museum/aceh> a sdp:StateMuseum ;
    sdp:name "Museum Negeri Aceh"@id ;
    sdp:description "Museum tertua di Aceh."@id ;
    sdp:address "Jl. Sultan Mahmudsyah No. 12"@id ;
    sdp:locatedInCity res:city-banda-aceh ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:establishedYear "1915"^^xsd:gYear ;
    sdp:latitude "5.5483"^^xsd:decimal ;
    sdp:longitude "95.3238"^^xsd:decimal ;
    sdp:openingHours "Tu-Su 08:00-16:00" ;
    sdp:hasImage res:img-2, res:img-1 .

res:img-1 a sdp:Image ; sdp:imageIndex 1 ;
    sdp:imageUrl "/images/museums/aceh/1.jpg"^^xsd:anyURI .
res:img-2 a sdp:Image ; sdp:imageIndex 2 ;
    sdp:imageUrl "/images/museums/aceh/2.jpg"^^xsd:anyURI .

res:city-banda-aceh a sdp:City ; sdp:name "Banda Aceh"@id .
res:province-aceh a sdp:Province ; sdp:name "Aceh"@id .

# Museum dengan data minim: tidak boleh menghasilkan null.
<https://museumsumatera.id/resource/museum/minim> a sdp:StateMuseum ;
    sdp:name "Museum Minim"@id .
"""


@pytest.fixture(scope="module")
def store() -> MuseumStore:
    return MuseumStore.dari_turtle(data=TTL)


@pytest.fixture(scope="module")
def doc(store) -> dict:
    return museum_jsonld(store, "aceh", BASIS)


def _ada_null(nilai) -> bool:
    if nilai is None:
        return True
    if isinstance(nilai, dict):
        return any(_ada_null(v) for v in nilai.values())
    if isinstance(nilai, list):
        return any(_ada_null(v) for v in nilai)
    return False


# ------------------------------------------------------------- bentuk dokumen


def test_tipe_dan_konteks_schema_org(doc):
    assert doc["@context"] == "https://schema.org"
    assert doc["@type"] == "Museum"
    assert doc["@id"] == str(IRI)


def test_url_halaman_absolut(doc):
    assert doc["url"] == "https://contoh.test/museum/aceh"


def test_gambar_absolut_dan_terurut(doc):
    assert doc["image"] == [
        "https://contoh.test/images/museums/aceh/1.jpg",
        "https://contoh.test/images/museums/aceh/2.jpg",
    ]


def test_alamat_dan_geo(doc):
    assert doc["address"] == {
        "@type": "PostalAddress",
        "streetAddress": "Jl. Sultan Mahmudsyah No. 12",
        "addressLocality": "Banda Aceh",
        "addressRegion": "Aceh",
        "addressCountry": "ID",
    }
    assert doc["geo"]["@type"] == "GeoCoordinates"
    assert doc["geo"]["latitude"] == pytest.approx(5.5483)


def test_jam_buka_hanya_bila_ada(store, doc):
    assert doc["openingHours"] == "Tu-Su 08:00-16:00"
    assert "openingHours" not in museum_jsonld(store, "minim", BASIS)


def test_museum_minim_tanpa_null(store):
    minim = museum_jsonld(store, "minim", BASIS)
    assert minim["name"] == "Museum Minim"
    assert not _ada_null(minim)
    assert "geo" not in minim and "address" not in minim and "image" not in minim


def test_slug_tidak_ada_atau_tidak_sah(store):
    assert museum_jsonld(store, "tidak-ada", BASIS) is None
    assert museum_jsonld(store, "'; DROP", BASIS) is None


# ------------------------------------------------------------------ round-trip


# Pasangan (properti sdp di graf asal, jalur schema.org di JSON-LD).
PETA = [
    (SDP.name, [SCHEMA.name]),
    (SDP.description, [SCHEMA.description]),
    (SDP.address, [SCHEMA.address, SCHEMA.streetAddress]),
    (SDP.latitude, [SCHEMA.geo, SCHEMA.latitude]),
    (SDP.longitude, [SCHEMA.geo, SCHEMA.longitude]),
    (SDP.establishedYear, [SCHEMA.foundingDate]),
    (SDP.openingHours, [SCHEMA.openingHours]),
]


def _ikuti(g, awal, jalur):
    node = awal
    for p in jalur:
        node = g.value(node, p)
        if node is None:
            return None
    return node


def _setara(asal: Literal, balik: Literal) -> bool:
    if isinstance(asal.toPython(), Decimal):
        return float(asal) == pytest.approx(float(balik))
    return str(asal) == str(balik)


@pytest.mark.parametrize("sdp_prop,jalur", PETA, ids=[str(p).rsplit("#")[-1] for p, _ in PETA])
def test_round_trip_sama_dengan_graf_asal(store, doc, sdp_prop, jalur):
    g = ke_graf(doc)
    assert (IRI, RDF.type, SCHEMA.Museum) in g
    asal = store.asserted.value(IRI, sdp_prop)
    balik = _ikuti(g, IRI, jalur)
    assert asal is not None and balik is not None
    assert _setara(asal, balik), f"{sdp_prop}: {asal!r} != {balik!r}"


def test_round_trip_kota_dan_provinsi(store, doc):
    g = ke_graf(doc)
    alamat = g.value(IRI, SCHEMA.address)
    assert str(g.value(alamat, SCHEMA.addressLocality)) == "Banda Aceh"
    assert str(g.value(alamat, SCHEMA.addressRegion)) == "Aceh"


# ------------------------------------------------------------- data sungguhan


@pytest.fixture(scope="module")
def store_nyata() -> MuseumStore:
    return muat_store()


def test_seluruh_museum_nyata_tanpa_null_dan_punya_geo(store_nyata):
    koleksi = semua_museum_jsonld(store_nyata, BASIS)
    assert len(koleksi["@graph"]) == 28
    assert not _ada_null(koleksi)
    for m in koleksi["@graph"]:
        assert m["@type"] == "Museum"
        assert "geo" in m, m["name"]
        assert m["image"], m["name"]


# ---------------------------------------------------------------------- web


@pytest.fixture()
def client(store):
    app.dependency_overrides[get_store] = lambda: store
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_endpoint_jsonld(client):
    r = client.get("/api/museum/aceh.jsonld")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/ld+json")
    data = r.json()
    assert data["@type"] == "Museum"
    assert data["url"].endswith("/museum/aceh")


def test_endpoint_jsonld_404(client):
    r = client.get("/api/museum/tidak-ada.jsonld")
    assert r.status_code == 404
    assert "error" in r.json()


def test_endpoint_semua_museum(client):
    r = client.get("/api/museum.jsonld")
    assert r.status_code == 200
    assert {m["name"] for m in r.json()["@graph"]} == {"Museum Negeri Aceh", "Museum Minim"}


def test_halaman_museum_menyisipkan_script_jsonld(client):
    html = client.get("/museum/aceh").text
    blok = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert len(blok) == 1
    data = json.loads(blok[0])
    assert data["name"] == "Museum Negeri Aceh"


def test_script_jsonld_tidak_bisa_menutup_tag_script(store):
    """Deskripsi berisi ``</script>`` tidak boleh memecah halaman (XSS)."""
    jahat = MuseumStore.dari_turtle(
        data=TTL.replace("Museum tertua di Aceh.", "</script><script>alert(1)</script>")
    )
    app.dependency_overrides[get_store] = lambda: jahat
    try:
        html = TestClient(app).get("/museum/aceh").text
    finally:
        app.dependency_overrides.clear()
    assert "<script>alert(1)" not in html
