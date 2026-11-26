"""Halaman /metode: kolom aturan penalaran dan angka fakta turunan yang konsisten.

Menanggapi catatan Ryan F (B2): ``fakta_turunan()`` kini membawa kunci
``aturan`` (mis. ``["rdfs9"]``). Halaman harus:

- menampilkan kolom "Aturan" di tabel fakta turunan,
- menampilkan angka fakta turunan yang **sama** dengan jumlah baris yang bisa
  ditelusuri (bukan ``len(closure) - len(asserted)`` yang memuat artefak),
- tetap jalan dengan ``fakta_turunan()`` versi lama yang belum punya ``aturan``.
"""

from __future__ import annotations

import re

import pytest
from fastapi.testclient import TestClient

import main
from main import app, get_store
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
sdp:StateMuseum rdfs:subClassOf sdp:Museum .
<https://museumsumatera.id/resource/museum/aceh> a sdp:StateMuseum ;
    sdp:name "Museum Negeri Aceh"@id .
"""


def _fakta(i: int, aturan: list[str] | None) -> dict:
    f = {
        "subjek": f"https://museumsumatera.id/resource/x{i}",
        "predikat": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "objek": "https://museumsumatera.id/ontology#Museum",
        "subjek_n3": f"res:x{i}",
        "predikat_n3": "rdf:type",
        "objek_n3": "sdp:Museum",
    }
    if aturan is not None:
        f["aturan"] = aturan
    return f


# Bentuk keluaran B2: 30 prp-inv, 4 rdfs2, 3 rdfs9, 2 dua-jalur.
FAKTA_B2 = (
    [_fakta(i, ["prp-inv"]) for i in range(30)]
    + [_fakta(100 + i, ["rdfs2"]) for i in range(4)]
    + [_fakta(200 + i, ["rdfs9"]) for i in range(3)]
    + [_fakta(300 + i, ["rdfs2", "rdfs9"]) for i in range(2)]
)
FAKTA_LAMA = [_fakta(i, None) for i in range(5)]


@pytest.fixture()
def client_dengan(monkeypatch):
    store = MuseumStore.dari_turtle(data=TTL)

    def _buat(fakta: list[dict]) -> TestClient:
        monkeypatch.setattr(main, "fakta_turunan", lambda s, subjek=None, batas=50: fakta[:batas])
        app.dependency_overrides[get_store] = lambda: store
        return TestClient(app)

    yield _buat
    app.dependency_overrides.clear()


def _baris_tabel(html: str) -> list[list[str]]:
    tbody = re.search(r'<table class="turunan">.*?<tbody>(.*?)</tbody>', html, re.S).group(1)
    return [
        [re.sub(r"<[^>]+>", "", sel).strip() for sel in re.findall(r"<td>(.*?)</td>", tr, re.S)]
        for tr in re.findall(r"<tr>(.*?)</tr>", tbody, re.S)
    ]


def test_kolom_aturan_ditampilkan(client_dengan):
    html = client_dengan(FAKTA_B2).get("/metode").text
    assert '<th scope="col">Aturan</th>' in html
    baris = _baris_tabel(html)
    assert all(len(b) == 4 for b in baris)
    assert "rdfs2, rdfs9" in {b[3] for b in baris}


def test_contoh_mewakili_setiap_aturan(client_dengan):
    """30 baris prp-inv tidak boleh menenggelamkan aturan lain dari 20 contoh."""
    baris = _baris_tabel(client_dengan(FAKTA_B2).get("/metode").text)
    assert len(baris) == 20
    assert {b[3] for b in baris} == {"prp-inv", "rdfs2", "rdfs9", "rdfs2, rdfs9"}


def test_angka_kartu_sama_dengan_fakta_yang_bisa_ditelusuri(client_dengan):
    html = client_dengan(FAKTA_B2).get("/metode").text
    kartu = re.search(
        r'Fakta turunan informatif</div>\s*<div class="angka">([\d.]+)</div>', html
    )
    assert kartu and kartu.group(1) == "39"
    assert "Contoh fakta turunan (39 total)" in html


def test_ringkasan_per_aturan_menghitung_dua_jalur(client_dengan):
    data = client_dengan(FAKTA_B2).get("/api/metode").json()
    assert data["ringkasan_turunan"] == {
        "informatif": 39,
        "per_aturan": {"prp-inv": 30, "rdfs2": 6, "rdfs9": 5},
        "dua_jalur_atau_lebih": 2,
    }


def test_halaman_menyebut_selisih_closure_sebagai_artefak(client_dengan):
    html = client_dengan(FAKTA_B2).get("/metode").text
    assert "Selisih closure" in html
    assert "owl:sameAs" in html


def test_tetap_jalan_tanpa_kunci_aturan(client_dengan):
    """fakta_turunan versi lama (sebelum B2 di-merge) tidak boleh merusak halaman."""
    client = client_dengan(FAKTA_LAMA)
    r = client.get("/metode")
    assert r.status_code == 200
    baris = _baris_tabel(r.text)
    assert len(baris) == 5 and all(b[3] == "—" for b in baris)
    data = client.get("/api/metode").json()
    assert data["ringkasan_turunan"]["per_aturan"] == {}
    assert data["ringkasan_turunan"]["informatif"] == 5


def test_tanpa_fakta_turunan(client_dengan):
    r = client_dengan([]).get("/metode")
    assert r.status_code == 200
    assert '<table class="turunan">' not in r.text
